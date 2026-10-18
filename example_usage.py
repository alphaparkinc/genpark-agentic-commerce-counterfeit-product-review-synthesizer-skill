from client import AgenticCommerceReviewAuthenticitySentinel

def main():
    sentinel = AgenticCommerceReviewAuthenticitySentinel()
    stream = [
        {"rating": 5, "text": "Amazing product! Item arrived fast great seller", "verified_purchase": False},
        {"rating": 4, "text": "Works as described, sturdy aluminium construction.", "verified_purchase": True},
        {"rating": 2, "text": "Cable started fraying after two weeks of normal desk use.", "verified_purchase": True}
    ]
    res = sentinel.audit_product_reviews("Magnetic Desk Charger", stream)
    print("--- E-Commerce Review Authenticity Sentinel ---")
    print(f"Product: {res['product_title']} | Grade: {res['authenticity_grade']}")
    print(f"Raw Rating: {res['raw_average_rating']} / 5.0 -> Authentic Adjusted: {res['adjusted_authentic_rating']} / 5.0")
    print(f"Authenticity Index: {res['authenticity_index']}%")

if __name__ == "__main__":
    main()
