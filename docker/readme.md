# 基本操作
## 容器操作
* 查看运行中的容器：docker ps
* 查看所有容器：docker ps -a
* 关闭指定容器：docker stop <container_id_or_name>
* 清理单个容器：docker rm <container_id_or_name>
* 清理所有停止的容器：docker container prune

# 常见Server的启动
## Mysql
### doc
* https://dev.mysql.com/doc/refman/8.4/en/docker-mysql-getting-started.html
### run
* docker pull container-registry.oracle.com/mysql/community-server
* docker run -p 3306:3306 --name=mysql container-registry.oracle.com/mysql/community-server
* docker logs mysql 2>&1 | grep GENERATED
* docker exec -it mysql mysql -uroot -p
* alter user USER() identified by 'root';

## Redis
### doc
* https://redis.io/docs/latest/operate/oss_and_stack/install/install-stack/docker/
### run
* docker run --name redis -p 6379:6379 redis
* docker exec -it redis redis-cli

## MongoDB
### doc
* https://www.mongodb.com/docs/manual/tutorial/install-mongodb-community-with-docker/
### run
* docker pull mongodb/mongodb-community-server
* docker run --name mongodb -p 27017:27017 mongodb/mongodb-community-server

## Prometheus
### doc
* https://prometheus.io/docs/prometheus/latest/getting_started/
### run
* docker pull prom/prometheus
* docker run -p 9090:9090 --name=prometheus -v ~/prometheus/prometheus.yaml:/etc/prometheus/prometheus.yaml prom/prometheus

## Grafana
### doc
* https://grafana.com/docs/grafana/latest/
### run
* docker pull grafana/grafana-enterprise
* docker run -p 3000:3000 --name=grafana grafana/grafana-enterprise
* user/pass: admin/admin

## Etcd
### doc
* https://etcd.io/docs/v3.6/op-guide/container/
### run
* docker pull gcr.io/etcd-development/etcd:v3.6.0
* 按照官方的脚本，无法启动，报端口占用，但实际上端口并没有被占用
