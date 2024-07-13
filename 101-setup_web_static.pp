# This Manifest installs Nginx server into server
exec { 'apt_update':
  command => '/usr/bin/apt update',
}

package { 'nginx':
  ensure => installed,
}

$nginx_config_content = @(EOF)
server {
    listen 80;
    server_name static_web;
    root /;
    location / {
        try_files $uri $uri/ =404;
	add_header X-Served-By $hostname;
    }

    location /hbnb_static {
        alias /data/web_static/current/;
	      try_files $uri $uri/ =404;
	      add_header X-Served-By $hostname;
    }
}
EOF

file { '/etc/nginx/sites-available/default':
  ensure  => present,
  content => $nginx_config_content,
  notify  => Service['nginx'],
}

exec { 'making directory_1':
  command => 'mkdir -p /data/web_static/shared',
  creates => '/data/web_static/shared',
  path    => ['/bin', '/usr/bin'],
}
exec { 'making directory_2':
  command => 'mkdir -p /data/web_static/releases/test/',
  path    => ['/bin', '/usr/bin'],
}

$test_content = @(EOF)
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOF

file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => $test_content,
}



exec { 'symbolic link':
  command => 'ln -sfr /data/web_static/releases/test/ /data/web_static/current',
  path    => ['/bin', '/usr/bin'],
}

exec { 'changing ownership':
  command => 'chown -hR ubuntu:ubuntu /data',
  path    => ['/bin', '/usr/bin'],
}

service { 'nginx':
  ensure  => running,
  enable  => true,
  require => Package['nginx'],
}
