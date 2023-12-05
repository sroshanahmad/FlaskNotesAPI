# FlaskNotesAPI
Flask application for managing notes via RESTful API. It is deployed using gunicorn as WSGI server and uses Ubuntu VM as deployment environment using qmeu-kvm. Nginx is used as reverse proxy.

API is consumed by web app which is built in ReactJs.

To checkout:
https://github.com/sroshanahmad/ReactNotesViewer

## Setting up Deployment environment:

1. Check if virtualization is supported:
lscpu | grep Virtualization
no output means virtualization is not supported

2. check if virtualization is enabled
kvm-ok

3. Install qemu-kvm and libvirt, will use libvirt to manage vms:
sudo apt install qemu-kvm libvirt-daemon-system

4. Check if user is in added to kvm group:
groups
lists name of groups user is in, if libvirt is not present then you need to add user

5. add user to kvm
sudo adduser $USER kvm
reboot for changes to take effect

6. to check if libvirt is working, we can use virsh command which is provided by libvirt:
virsh list -all
if no vms is present it will display none. used just to check.

7. To install vm:
sudo virt-install \ 
--name <your_vm_name> \
--memory <ram size for vm> \
--vcpus 2 \
--cpu host \
--disk size=<disk space for iso>,path=/var/lib/libvirt/images/<your_vm_name.qcow2>,format=qcow2 \
--network bridge=virbr0,model=virtio \
--graphics spice \
--console pty,target_type=serial \
--location <full path to iso file or  give this 'http://releases.ubuntu.com/20.04/ubuntu-20.04-live-server-amd64.iso'> \
--extra-args 'console=ttyS0,115200n8 serial'

You can also use virt-manager which is GUI for kvm.
To install virt-manager:
sudo apt install virt-manager

8. To start vm:
virsh start <your_vm_name>

8. To stop vm:
virsh stop <your_vm_name>

## Setting up Gunicorn:

Head to flask-app directory.

1. Activate python virtual environment:

source venv/bin/activate

2. Install gunicorn:
pip install gunicorn

3. To create service file for gunicorn
sudo touch /etc/systemd/system/<file_name>.service

content for <file_name>.service:
It is recommened to create a different user to run server and not run this as root. 
[Unit]
Description=Gunicorn instance to serve Flask app
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=<full_path_to flask-app>
Environment="PATH=<full_path_to flask-app>/venv/bin"
ExecStart=<full_path_to flask-app>/venv/bin/gunicorn -w 4 --reload -b <ipaddres>:8000 website.main:app

[Install]
WantedBy=multi-user.target


4. Enable the Service to run when the system boots:
sudo systemctl enable <file_name>.service

5. To start the service: 
sudo systemctl start <file_name>.service

6. check the status of your service:
sudo systemctl status <file_name>.service

7. Any changes to the systemd service file require you to reload the systemd manager configuration. This can be done with the command:
sudo systemctl daemon-reload

8. Followed by restarting the service:
sudo systemctl restart gunicorn.service



## Setting up Nginx:

1. Install nginx:
sudo apt install nginx

2. edit cofiguration file at /etc/nginx/sites-available/default with:

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

Note:
If you are using react, you will have to run:
npm run build

and provide the index.html inside the build folder.

3. Enable site (if using new config file):
sudo ln -s /etc/nginx/sites-available/<filename> /etc/nginx/sites-enabled/

4. Check for syntax error:
sudo nginx -t

5. Reload nginx to  apply change:
sudo systemctl reload nginx

6. Enable nginx to start when system boots: 
sudo systemctl enable nginx

Check it on the ip address it is up.!!

Note:
If you are getting 404 file error first time when you try access site, it might because nginx doesnt have read access to the files and directories to where your index.html is. You have to provide access to all parent directories:
sudo chmod -R 755 <directories> 

Then restart nginx for changes to take place.

## API Endpoints:

1. To list all notes:
<ip>/api/notes

2. To retreive a note:
<ip>/api/notes/<id>

3. To create a note:
<ip>/api/notes

Takes 'data' as note content to create note.

4. To update a note:
<ip>/notes/<id>
Takes 'data' to update note's content .

5. To delete a note:
<ip>/notes/<id>
