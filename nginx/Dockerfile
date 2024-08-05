FROM nginx:stable-alpine


# COPY nginx-certificate.crt /etc/nginx/ssl/nginx-selfsigned.crt
# COPY nginx.key /etc/nginx/ssl/nginx-selfsigned.key
COPY nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]