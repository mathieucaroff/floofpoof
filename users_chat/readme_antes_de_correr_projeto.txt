Antes de correr o projeto install/update as seguintes packages:

1. update pip: python -m pip install -U pip
2. update setuptools: pip install -U setuptools
3. install channels: pip install channels
4. install redis (in python side): pip install redis
5. install channels-redis: pip install channels-redis

6. run a redis server on windows:
	a) https://github.com/microsoftarchive/redis/releases
	b) download the 3.0.504 version zip file
	c) create a folder(name=Redis) in your C:\
	d) extract the zip file content in the Redis folder
	e) add the Redis folder to your windows path... -->> this shows how (https://stackoverflow.com/questions/44272416/how-to-add-a-folder-to-path-environment-variable-in-windows-10-with-screensho)
	f) open a separate cmd window and run: redis-server C:\Redis\redis.windows.conf
	g) in a separate cmd window run your Django project