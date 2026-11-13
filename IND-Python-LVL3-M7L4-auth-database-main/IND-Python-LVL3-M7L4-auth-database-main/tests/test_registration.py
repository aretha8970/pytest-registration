import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Fixture untuk menyiapkan database sebelum pengujian dan membersihkannya setelah selesai."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Fixture untuk mendapatkan koneksi database dan menutupnya setelah pengujian."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Menguji pembuatan database dan tabel pengguna."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Tabel 'users' harus ada dalam database."

def test_add_new_user(setup_database, connection):
    """Menguji penambahan pengguna baru."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Pengguna harus ditambahkan ke database."

# Berikut adalah pengujian yang bisa ditulis:
def test_add_same_user(setup_database, connection):
    "Menguji percobaan menambahkan pengguna dengan nama pengguna yang sudah ada."
    add_user('testuser', 'testuser@example.com', 'password123')
    user2= add_user('testuser', 'wtv@example.com', 'password321')
    assert user2 is False
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user != user2, "tidak boleh pakai username yg sama."

def test_authenticate_user(setup_database, connection):
    """Menguji keberhasilan autentikasi pengguna."""
    add_user('testuser', 'testuser@example.com', 'password123')
    assert authenticate_user('testuser', 'password123') is True, "anda berhasil utk login"

def test_authenticate_not_user(setup_database, connection):
    """Menguji autentikasi pengguna yang tidak ada."""
    assert authenticate_user('amu', 'OWO') is False, "user tdk ada"

def test_authenticate_user_fail(setup_database, connection):
    """Menguji autentikasi dengan kata sandi yang salah."""
    add_user('testuser', 'testuser@example.com', 'password123')
    assert authenticate_user('testuser', 'OWO') is False, "anda gagal utk login"

def test_display_user(setup_database, connection):
    """Menguji tampilan yang benar dari daftar pengguna"""
    add_user('testuser', 'testuser@example.com', 'password123')
    add_user('amu', 'wtv@example.com', 'password321')
    assert display_users() 
