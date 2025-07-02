from decimal import Decimal

from app.models import Parcel, PricingRule


def calculate_price(parcel: Parcel, pricing_rule: PricingRule, distance_km: float) -> Decimal:
    base = pricing_rule.base_rate or Decimal(0)
    weight_kg = parcel.weight_kg or Decimal(0)
    rate_per_kg = pricing_rule.rate_per_kg or Decimal(0)
    rate_per_km = pricing_rule.rate_per_km or Decimal(0)

    weight_price = weight_kg * rate_per_kg
    distance_price = Decimal(distance_km) * rate_per_km

    total = base + weight_price + distance_price
    return total.quantize(Decimal("0.01"))
