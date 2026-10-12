def test_post_car_returns_201_and_json(client):
    payload = {"make": "Ford", "model": "Fiesta", "year": 2018, "color": "Black"}
    response = client.post("/api/cars", json=payload)
    
    assert response.status_code == 201
    car = response.json()
    assert car["id"] > 0
    assert car["make"] == "Ford"
    assert car["model"] == "Fiesta"
    assert response.headers["location"] == f"/api/cars/{car['id']}"


def test_invalid_year_is_not_saved(client):
    # 发送年份为 1800 的无效数据
    payload = {"make": "Ford", "model": "Fiesta", "year": 1800, "color": "Black"}
    response = client.post("/api/cars", json=payload)
    
    # 断言返回 422 错误
    assert response.status_code == 422
    
    # 发送 GET 请求，断言数据库里确实没有保存这辆车
    response = client.get("/api/cars")
    assert response.json() == []