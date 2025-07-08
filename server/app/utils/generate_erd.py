from graphviz import Digraph

dot = Digraph(comment="Lightning Express ERD", format="png")
dot.attr(rankdir="TB", fontsize="12")

# 📦 Nodes (Tables)
dot.node("User", "User\nid, username, email, user_type_id, ...")
dot.node("Parcel", "Parcel\nid, tracking_number, sender_id, ...")
dot.node("Delivery", "Delivery\nid, parcel_id, driver_id, ...")
dot.node("TrackingUpdate", "TrackingUpdate\nid, parcel_id, event_type, ...")
dot.node("Vehicle", "Vehicle\nid, license_plate, vehicle_type_id, ...")
dot.node("VehicleType", "VehicleType\nid, name")
dot.node("Branch", "Branch\nid, name, address, ...")
dot.node("Payment", "Payment\nid, parcel_id, payment_method, ...")
dot.node("PricingRule", "PricingRule\nid, name, rate_per_kg, ...")
dot.node("BranchHistory", "BranchHistory\nid, parcel_id, branch_id, ...")

# 🔗 Relationships (Edges)
dot.edge("User", "Parcel", label="1 : * sender_id")
dot.edge("User", "Delivery", label="1 : * driver_id")
dot.edge("Parcel", "Delivery", label="1 : 1 parcel_id")
dot.edge("Parcel", "TrackingUpdate", label="1 : * parcel_id")
dot.edge("Parcel", "Branch", label="* : 1 current_branch_id")
dot.edge("Vehicle", "Branch", label="* : 1 current_branch_id")
dot.edge("VehicleType", "Vehicle", label="1 : * vehicle_type_id")
dot.edge("Parcel", "Payment", label="1 : 1 parcel_id")
dot.edge("Delivery", "PricingRule", label="* : 1 pricing_rule_id")
dot.edge("BranchHistory", "Parcel", label="* : 1 parcel_id")
dot.edge("BranchHistory", "Branch", label="* : 1 branch_id")
dot.edge("TrackingUpdate", "Branch", label="* : 1 branch_id")

# 💾 Save and render
dot.render("../../models_erd", cleanup=True)
print("✅ ER Diagram generated as models_erd.png")
