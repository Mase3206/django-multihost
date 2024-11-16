make groups
make install
mkdir /django/fall24
create-group fall24 group1
cd ../fall24/group1

deploy prep -r https://github.com/mase3206/group-awesome.git -g group1 -s group1 -y
