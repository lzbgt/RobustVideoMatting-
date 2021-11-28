rm -fr build
mkdir build
cp ../.env build/
cp -fr ../app build/app
cp -f ../inference*.py build/
cp -f ../rvm_* build/
cp -fr ../model build/
docker build -t app .
