server:
  #!/usr/bin/env sh
  cd "$(git rev-parse --show-toplevel)/src/website"
  uvicorn src.website.website.asgi:application --reload

virtualenv:
  #!/usr/bin/env sh
  cd "$(git rev-parse --show-toplevel)"
  pwd
  source .venv/bin/activate

deploy:
  #!/usr/bin/env sh
  docker buildx build --platform linux/amd64 -t jordan-online-portfolio:latest .
  docker tag jordan-online-portfolio:latest 886149544017.dkr.ecr.us-west-2.amazonaws.com/websites/jordan-online-portfolio:latest
  aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 886149544017.dkr.ecr.us-west-2.amazonaws.com
  docker push 886149544017.dkr.ecr.us-west-2.amazonaws.com/websites/jordan-online-portfolio:latest
  kubectl rollout restart deployment jordan-online-portfolio


apply-k8s:
  #!/usr/bin/env sh
  kubectl apply -f k8s/deployment.yaml
  kubectl apply -f k8s/service.yaml
  kubectl apply -f k8s/ingress.yaml