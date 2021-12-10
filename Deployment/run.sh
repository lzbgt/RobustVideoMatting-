sudo docker run -d --gpus all --name rvmapp  -p 30100:5000  -v `pwd`/.env:/build/.env  lzbgt/rvmapp:cuda
