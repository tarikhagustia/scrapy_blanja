from datetime import datetime

from scrapy.utils.project import get_project_settings
from sqlalchemy import (
    Integer, String, DateTime, Float, Date)
from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"), pool_size=10, max_overflow=20)


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class ProductDB(DeclarativeBase):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer)
    shop_id = Column(Integer)
    kategori = Column(Integer)
    kategori_text = Column(String(255))
    sub_kategori = Column(Integer)
    sub_kategori_text = Column(String(100))
    sub_kategori_child = Column(String(100))
    name = Column(String(255))
    url = Column(String(255))
    image_url = Column(String(255))
    price = Column(Float)
    original_price = Column(Float)
    created = Column(DateTime)
    updated = Column(DateTime)

    def __repr__(self):
        return "<Product(id='%s', name='%s')>" % (
            self.product_id, self.name)


class ShopDB(DeclarativeBase):
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    url = Column(String(255))
    location = Column(String(255))
    city = Column(String(255))
    created = Column(DateTime)
    updated = Column(DateTime)


class TransactionDB(DeclarativeBase):
    __tablename__ = "product_transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer)
    shop_id = Column(Integer)
    date = Column(Date)
    produk_yang_terjual = Column(Integer)
    transaksi_sukses = Column(Integer)
    transaksi_dibatalkan = Column(Integer)
    dilihat = Column(Integer)
    count_review = Column(Integer)
    rating = Column(Integer)
    created = Column(DateTime)
    updated = Column(DateTime)

    def __str__(self):
        return "<{}, {}>".format(self.__class__, self.date)


class DetailProductDB(DeclarativeBase):
    __tablename__ = "detail_product_transactions"

    product_id = Column(Integer, primary_key=True)
    shop_id = Column(Integer)
    produk_yang_terjual = Column(Integer)
    transaksi_sukses = Column(Integer)
    transaksi_dibatalkan = Column(Integer)
    dilihat = Column(Integer)
    count_review = Column(Integer)
    rating = Column(Integer)
    created = Column(DateTime)
    updated = Column(DateTime)


class DailyTransactionDB(DeclarativeBase):
    __tablename__ = "product_transactions_harian"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer)
    shop_id = Column(Integer)
    date = Column(Date)
    produk_yang_terjual = Column(Integer)
    transaksi_sukses = Column(Integer)
    transaksi_dibatalkan = Column(Integer)
    dilihat = Column(Integer)
    count_review = Column(Integer)
    rating = Column(Integer)
    created = Column(DateTime)
    updated = Column(DateTime)

    def __str__(self):
        return "<{}, {}>".format(self.__class__, self.date)


class CategoryDB(DeclarativeBase):
    __tablename__ = "kategori"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_core = Column(Integer, primary_key=True)
    parent_id = Column(Integer)
    market_id = Column(Integer, default=1)
    url = Column(String)
    text = Column(String)
    fa_icon = Column(String, default="")
    image = Column(String, default="")
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class ShopSalesTotalDB(DeclarativeBase):
    __tablename__ = "shop_total_penjualan"

    shop_id = Column(Integer, primary_key=True)
    total_penjualan = Column(Float(10))
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now())


class CategoryTransactionDB(DeclarativeBase):
    __tablename__ = "kategori_transactions_harian"

    id = Column(Integer, primary_key=True, autoincrement=True)
    kategori_id = Column(Integer)
    date = Column(Date, default=datetime.now().date())
    produk_yang_terjual = Column(Integer)
    transaksi_sukses = Column(Integer)
    transaksi_dibatalkan = Column(Integer)
    dilihat = Column(Integer)
    count_review = Column(Integer)
    rating = Column(Integer)
    min_harga = Column(Float)
    max_harga = Column(Float)
    jml_produk = Column(Integer)
    jml_toko = Column(Integer)
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now())

    def __str__(self):
        return "<{}, {}>".format(self.__class__, self.date)


class SubCategoryTransactionDB(DeclarativeBase):
    __tablename__ = "sub_kategori_transactions_harian"

    id = Column(Integer, primary_key=True, autoincrement=True)
    kategori_id = Column(Integer)
    date = Column(Date, default=datetime.now().date())
    produk_yang_terjual = Column(Integer)
    transaksi_sukses = Column(Integer)
    transaksi_dibatalkan = Column(Integer)
    dilihat = Column(Integer)
    count_review = Column(Integer)
    rating = Column(Integer)
    min_harga = Column(Float)
    max_harga = Column(Float)
    jml_produk = Column(Integer)
    jml_toko = Column(Integer)
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now())

    def __str__(self):
        return "<{}, {}>".format(self.__class__, self.date)
