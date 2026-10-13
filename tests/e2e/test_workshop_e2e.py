import re
from playwright.sync_api import expect


def test_user_creates_car_in_browser(page, live_server):
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Toyota")
    page.get_by_label("Model", exact=True).fill("Yaris")
    page.get_by_label("Year", exact=True).fill("2020")
    page.get_by_label("Color", exact=False).fill("Blue")
    page.get_by_role("button", name="Create car").click()

    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
    expect(page.get_by_role("heading", name="Toyota Yaris")).to_be_visible()


def test_user_edits_car_and_change_survives_reload(page, live_server):
    # 1. 创建 Honda Civic (2022)
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Honda")
    page.get_by_label("Model", exact=True).fill("Civic")
    page.get_by_label("Year", exact=True).fill("2022")
    page.get_by_role("button", name="Create car").click()
    
    # 断言创建成功，跳转到了详情页
    expect(page.get_by_role("heading", name="Honda Civic")).to_be_visible()

    # 2. 点击 Edit car 链接进入编辑页面
    page.get_by_role("link", name="Edit car").click()

    # 3. 修改 Model 为 Accord，年份改为 2023
    page.get_by_label("Model", exact=True).fill("Accord")
    page.get_by_label("Year", exact=True).fill("2023")

    # 4. 点击 Save changes 按钮保存
    page.get_by_role("button", name="Save changes").click()

    # 5. 强制等待 URL 跳转到详情页
    page.wait_for_url(re.compile(r"/cars/\d+$"))

    # 6. 关键修改：直接等待 #car-title 元素的文本变成 Honda Accord
    # 注意：这里不再用 get_by_role("heading")，而是用 id 定位器，且超时时间延长到 30000 毫秒（30秒）
    expect(page.locator("#car-title")).to_have_text("Honda Accord", timeout=30000)

    # 7. 刷新页面 (Reload)
    page.reload()

    # 8. 断言刷新后，页面显示的内容依然是修改后的 Accord 和 2023
    expect(page.locator("#car-model")).to_have_text("Accord", timeout=30000)
    expect(page.locator("#car-year")).to_have_text("2023", timeout=30000)