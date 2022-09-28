set terminal png size 600
set output "dumb_http_server_mt_ab.png"
set title "100 requests, 20 concurrent requests"
set size ratio 0.6
set grid y
set xlabel "requests"
set ylabel "response time (ms)"
plot "dumb_http_server_mt_ab.csv" using 9 smooth sbezier with lines title "http://192.168.10.199:8080/"
