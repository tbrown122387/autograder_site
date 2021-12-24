docker compose up -d server
until docker logs grading-site-api 2>&1 | grep -q "Application startup complete"; do
    echo "Waiting for startup..."
    sleep 1;
done;
docker exec grading-site-api python3 -m pytest
docker compose down