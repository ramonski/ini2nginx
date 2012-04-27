### Nginx config for VHM example.com ###
server {
    listen 80;
    server_name example.com www.example.com;

    # maintenance page
    error_page 503 @503;
    location @503 {
        rewrite  ^(.*)$  /system/maintenance.html break;
    }

    if (-f $document_root/system/maintenance.html) {
        return 503;
    }

    location / {
        proxy_set_header        Host            $http_host;
        proxy_set_header        X-Hosting       example.com;
        proxy_set_header        X-Real-IP       $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
        rewrite                 ^(.*)$ /VirtualHostBase/http/$host/example/VirtualHostRoot/$1 break;
        proxy_pass              http://localhost:8080;
    }
}
# vim: set ft=nginx ts=4 sw=4 expandtab :