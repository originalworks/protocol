docker build -t ow/iscc-repo . 
docker tag ow/iscc-repo:latest 595785979655.dkr.ecr.us-east-1.amazonaws.com/ow/iscc-repo:latest
docker push 595785979655.dkr.ecr.us-east-1.amazonaws.com/ow/iscc-repo:latest
