import enum
from sqlalchemy import Column, String, ForeignKey, Integer, Text, Boolean, DateTime, Numeric, Enum
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.base import Base


# * ====== Enum Definitions ======


class PaymentMethodEnum(str, enum.Enum):
    CASH_ON_DELIVERY = "cash_on_delivery"
    CREDIT_CARD = "credit_card"
    WALLET = "wallet"


class DeliveryStatusEnum(str, enum.Enum):
    SCHEDULED = "scheduled"
    PICKED_UP = "picked_up"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    FAILED_ATTEMPT = "failed_attempt"


class StatusDetailEnum(str, enum.Enum):
    ENTERED_SYSTEM = "entered_system"
    AT_SORTING_CENTER = "at_sorting_center"
    OUT_FOR_DELIVERY = "out_for_delivery"


class EventTypeEnum(str, enum.Enum):
    SCANNED_IN = "scanned_in"
    DEPARTED = "departed"
    ARRIVED = "arrived"
    DELIVERED = "delivered"


# * ====== Core Master Tables ======


class UserType(Base):
    __tablename__ = "user_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(
        String, unique=True, nullable=False
    )  # * e.g. 'customer', 'driver', 'admin', 'staff'
    description = Column(Text)

    users = relationship("User", back_populates="user_type_rel")


class VehicleType(Base):
    __tablename__ = "vehicle_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # * e.g. 'van', 'truck', 'motorcycle'
    description = Column(Text)

    vehicles = relationship("Vehicle", back_populates="vehicle_type_rel")


class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # * e.g. 'กรุงเทพฯ', 'เชียงใหม่'
    address = Column(Text)
    phone_number = Column(String)
    email = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    parcels_at_branch = relationship("Parcel", back_populates="current_branch")
    vehicles_at_branch = relationship("Vehicle", back_populates="current_branch")


class PricingRule(Base):
    __tablename__ = "pricing_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # * e.g. "Base Rate", "Distance Rate"
    base_rate = Column(Numeric(10, 2), nullable=True)  # * ค่าคงที่เริ่มต้น
    rate_per_kg = Column(Numeric(10, 2), nullable=True)
    rate_per_km = Column(Numeric(10, 2), nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# * ====== User and Related Entities ======


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    phone_number = Column(String)
    address = Column(Text)
    user_type_id = Column(Integer, ForeignKey("user_types.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_type_rel = relationship("UserType", back_populates="users")
    parcels_sent = relationship("Parcel", back_populates="sender")
    deliveries_assigned = relationship("Delivery", back_populates="driver")


# * ====== Parcel and Related Entities ======


class Parcel(Base):
    __tablename__ = "parcels"

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)

    weight_kg = Column(Numeric(10, 2))
    dimensions_cm = Column(String)  # * format: "10x20x30"
    declared_value = Column(Numeric(10, 2))

    # * ถ้าส่งโดย user จะ relation กับ user.id หรือ ถ้าส่งโดย anonymous ไม่มี relation กับ user.id
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    sender_name = Column(String)
    sender_address = Column(Text)
    sender_phone_number = Column(String)
    recipient_name = Column(String)
    recipient_address = Column(Text)
    recipient_phone_number = Column(String)

    current_branch_id = Column(Integer, ForeignKey("branches.id"))
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sender = relationship("User", back_populates="parcels_sent")
    payment = relationship("Payment", back_populates="parcel", uselist=False)
    current_branch = relationship("Branch", back_populates="parcels_at_branch")
    delivery = relationship("Delivery", back_populates="parcel", uselist=False)
    tracking_updates = relationship("TrackingUpdate", back_populates="parcel")
    branch_history = relationship("BranchHistory", back_populates="parcel")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    parcel_id = Column(Integer, ForeignKey("parcels.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)  # * ราคาชำระเงินของพัสดุ
    payment_method = Column(Enum(PaymentMethodEnum, name="payment_method_enum"), nullable=False)
    paid_at = Column(DateTime, nullable=True)
    is_paid = Column(Boolean, default=False)
    notes = Column(Text)

    parcel = relationship("Parcel", back_populates="payment")


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, index=True)
    parcel_id = Column(Integer, ForeignKey("parcels.id"), unique=True, nullable=False)
    driver_id = Column(Integer, ForeignKey("users.id"))
    start_location = Column(String)
    end_location = Column(String)
    scheduled_pickup_at = Column(DateTime)
    actual_pickup_at = Column(DateTime)
    scheduled_delivery_at = Column(DateTime)
    actual_delivery_at = Column(DateTime)
    delivery_status = Column(
        Enum(DeliveryStatusEnum, name="delivery_status_enum"),
        default=DeliveryStatusEnum.SCHEDULED,
        nullable=False,
    )
    cost = Column(Numeric(10, 2))  # * ค่าขนส่ง
    notes = Column(Text)
    pricing_rule_id = Column(Integer, ForeignKey("pricing_rules.id"))
    calculated_price = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    parcel = relationship("Parcel", back_populates="delivery")
    driver = relationship("User", back_populates="deliveries_assigned")
    pricing_rule = relationship("PricingRule")


class TrackingUpdate(Base):
    __tablename__ = "tracking_updates"

    id = Column(Integer, primary_key=True, index=True)
    parcel_id = Column(Integer, ForeignKey("parcels.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=True)
    location = Column(String)  # สถานที่ปัจจุบันของพัสดุ
    status_detail = Column(Enum(StatusDetailEnum, name="status_detail_enum"), nullable=True)
    event_type = Column(Enum(EventTypeEnum, name="event_type_enum"), nullable=True)

    parcel = relationship("Parcel", back_populates="tracking_updates")
    branch = relationship("Branch")


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String, unique=True, nullable=False)
    make = Column(String)
    model = Column(String)
    year = Column(Integer)
    capacity_kg = Column(Numeric(10, 2))
    vehicle_type_id = Column(Integer, ForeignKey("vehicle_types.id"), nullable=False)
    current_branch_id = Column(Integer, ForeignKey("branches.id"))  # * สาขาที่ยานพาหนะประจำอยู่
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    vehicle_type_rel = relationship("VehicleType", back_populates="vehicles")
    current_branch = relationship("Branch", back_populates="vehicles_at_branch")


class BranchHistory(Base):
    __tablename__ = "branch_history"

    id = Column(Integer, primary_key=True)
    parcel_id = Column(Integer, ForeignKey("parcels.id"), nullable=False)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False)
    arrived_at = Column(DateTime)
    departed_at = Column(DateTime)

    parcel = relationship("Parcel", back_populates="branch_history")
    branch = relationship("Branch")
