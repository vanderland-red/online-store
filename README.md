# 🛍️ Pinkerton Store

یک فروشگاه اینترنتی ساده و کاربردی که با **Python و Flask** توسعه داده شده است.
این پروژه شامل سیستم کاربران، محصولات، سبد خرید، سفارش‌ها و پرداخت آزمایشی است.

##  Features

* 👤 ثبت‌نام و ورود کاربران
* 🔐 احراز هویت با Flask-Login
* 🛍️ نمایش و جستجوی محصولات
* 🛒 افزودن و حذف محصولات از سبد خرید
* 📦 مدیریت سفارش‌ها
* 💳 سیستم پرداخت آزمایشی (Mock Gateway)
* 👤 داشبورد کاربر
* ✏️ ویرایش اطلاعات حساب کاربری
* 💬 ارسال پیشنهاد توسط کاربران
* 👨‍💼 پنل مدیریت
* ➕ افزودن و ویرایش محصولات
* 🖼️ آپلود تصویر محصولات
* 📊 مدیریت وضعیت سفارش‌ها
*  CSRF Protection
* 🗄️ مدیریت دیتابیس با SQLAlchemy و Flask-Migrate
* 📱 طراحی Responsive

##  Technologies

* **Python**
* **Flask**
* **Flask-SQLAlchemy**
* **Flask-Login**
* **Flask-WTF**
* **Flask-Migrate**
* **MySQL**
* **HTML5**
* **CSS3**
* **Jinja2**


## Database

دیتابیس پروژه با **MySQL** و **SQLAlchemy** پیاده‌سازی شده و برای مدیریت تغییرات ساختار دیتابیس از **Flask-Migrate** استفاده شده است.

## Installation

ابتدا Repository را Clone کنید:

```bash
git clone <repository-url>
cd Pinkerton-Store
```

محیط مجازی ایجاد و فعال کنید:

```bash
python -m venv venv
```

در Windows:

```bash
venv\Scripts\activate
```

سپس وابستگی‌ها را نصب کنید:

```bash
pip install -r requirements.txt
```

تنظیمات دیتابیس و متغیرهای موردنیاز پروژه را در فایل Configuration قرار دهید.

سپس برنامه را اجرا کنید:

```bash
python app.py
```

برنامه به صورت پیش‌فرض روی آدرس زیر اجرا می‌شود:

```text
http://127.0.0.1:5000
```

##  Admin Panel

پنل مدیریت امکان موارد زیر را فراهم می‌کند:

* افزودن محصول
* ویرایش محصول
* فعال یا غیرفعال کردن محصولات
* مشاهده سفارش‌ها
* تغییر وضعیت سفارش‌ها

##  Project Goal

هدف این پروژه تمرین و پیاده‌سازی مفاهیم **Backend Development، Authentication، E-commerce، Cart Management، Payment Flow و Database Management با Flask** بوده است.

---

###  Developed with Python & Flask

**Pinkerton Store**
