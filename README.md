# FlaskNotesAPI

## Overview
FlaskNotesAPI is a Flask application designed for managing notes through a RESTful API. It integrates with a ReactJS-based web application for the frontend. The backend is deployed using Gunicorn as a WSGI server on an Ubuntu VM, with QEMU-KVM for virtualization. Nginx serves as the reverse proxy.

The API is consumed by a ReactJs-based web application. Link to repo:

React Web App: [ReactNotesViewer](https://github.com/sroshanahmad/ReactNotesViewer)


## Deployment Environment Setup


### Prerequisites
- **Virtualization support check**: Run `lscpu | grep Virtualization`. No output indicates no support.
- **Verify Virtualization enablement**: Run `kvm-ok`.

### Virtualisation and VM Setup

1. **Install qemu-kvm and libvirt**: `sudo apt install qemu-kvm libvirt-daemon-system`.

2. **Verify user group membership**: Check if the user is in the `kvm` group with `groups`. Add with `sudo adduser $USER kvm` if not present.

3. **Verify libvirt functioning**: `virsh list -all`. Will display none if you don't have any vms installed.

4. **Virtual Machine Installation**: Use `virt-install` or `virt-manager` for GUI.
If using `virt-install`:
```
sudo virt-install \ 
--name <your_vm_name> \
--memory <ram size for vm> \
--vcpus 2 \
--cpu host \
--disk size=<disk space you want to give for iso>,path=/var/lib/libvirt/images/<your_vm_name.qcow2>,format=qcow2 \
--network bridge=virbr0,model=virtio \
--graphics spice \
--console pty,target_type=serial \
--location <full path to iso file> \
--extra-args 'console=ttyS0,115200n8 serial'
```
5. **Manage VM**: Start with `virsh start <vm_name>` and stop with `virsh stop <vm_name>`.

  
## Gunicorn Setup

### Flask App Preparation
1. **Activate Python virtual environment**: `source venv/bin/activate`.
2. **Install Gunicorn**: `pip install gunicorn`.

### Service File Creation
1. **Create a service file**: `sudo touch /etc/systemd/system/<file_name>.service`.
2. **Service file content**: Use a non-root user for the service. Populate the file with necessary details (see example below).
3. **Enable and Manage Service**: Enable (`sudo systemctl enable <file_name>.service`), start (`sudo systemctl start <file_name>.service`), check status (`sudo systemctl status <file_name>.service `), and reload (`sudo systemctl daemon-reload`) as needed.

- Any changes to the systemd service file require you to reload the systemd manager configuration. This can be done with the command: `sudo systemctl daemon-reload`
- Followed by restarting the service: `sudo systemctl restart gunicorn.service`



## Nginx Setup

### Installation and Configuration
1. **Install Nginx**: `sudo apt install nginx`.
2. **Edit Nginx Configuration**: Modify `/etc/nginx/sites-available/default`. Set up reverse proxy for Flask and static file handling for React (see example below).
3. **Enable Nginx Site**: If instead using/creating a different config file, link it to the sites-enabled directory by `sudo ln -s /etc/nginx/sites-available/<filename> /etc/nginx/sites-enabled/`
### Maintenance
- Check syntax: `sudo nginx -t`.
- Reload Nginx: `sudo systemctl reload nginx`.
- Enable Nginx on boot: `sudo systemctl enable nginx`.
-  Adjust permissions 


**Check it on the ip address it is up.!!**

- **Note**
**Access and permission issues**:if 404 errors occurs first time when you try access site, it might because nginx doesnt have read access to the files and to directories to where your index.html is. You have to provide access to all parent directories:
`sudo chmod -R 755 <directories>` 

    Then restart nginx for changes to take place.

## API Endpoints:

1. **List All Notes**: `<ip>/api/notes`
2. **Retrieve a Note**: `<ip>/api/notes/<id>`.
3. **Create a Note**: `<ip>/api/notes` (POST with 'data')
4. **Update a Note**: `<ip>/api/notes/<id>` (PUT with 'data')
5. **Delete a Note**: `<ip>/api/notes/<id>`.

---
**Note**: Replace `<placeholders>` with actual values.

- Service file example for Gunicorn:
    ```
    [Unit]
    Description=Gunicorn instance to serve Flask app
    After=network.target

    [Service]
    User=<user>
    Group=www-data
    WorkingDirectory=<path_to_flask_app>
    Environment="PATH=<path_to_venv>"
    ExecStart=<path_to_gunicorn> -w 4 --reload -b <ip>:8000 <app_module>

    [Install]
    WantedBy=multi-user.target
    ```
- Configuration setting for Nginx:

    **Note**: If you are using react, you will have to run:
    `npm run build` and provide the index.html inside the build folder.

    ```
    server {
        # listen [::]:80 default_server; # by default. this will listen on all n/w interfaces on port 80 for both ipv4 and ipv6 
        listen <ip address>;
        root <directory to react index.html>;
        index index.html;
        server_name _;
        location / {
            try_files $uri $uri/ /index.html;
        }
        # Additional configuration for handling static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico)$ {
            expires max;
            log_not_found off;
        }
        # Reverse proxy for Flask application
        location /api/ {
            proxy_pass http://127.0.0.1:8000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }
    }
    ```
