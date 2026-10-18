"""
Agentic Commerce Review Authenticity Sentinel (Pure Stdlib)
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
from typing import Dict, Any, List

class AgenticCommerceReviewAuthenticitySentinel:
    SUSPICIOUS_PHRASES = {
        "received this product for free", "honest review in exchange", "item arrived fast great seller",
        "best purchase ever five stars", "highly recommend buy now"
    }

    def __init__(self, sentinel_name: str = "GenPark-ReviewGuard-Core"):
        self.sentinel_name = sentinel_name

    def audit_product_reviews(self, product_title: str, reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not reviews:
            return {"verdict": "NO_REVIEWS_FOUND", "adjusted_rating": 0.0}
            
        raw_ratings = [float(r.get("rating", 5.0)) for r in reviews]
        raw_avg = sum(raw_ratings) / len(raw_ratings)
        
        valid_reviews = []
        flagged_reviews_count = 0
        
        for r in reviews:
            text = r.get("text", "").lower()
            verified = bool(r.get("verified_purchase", True))
            rating = float(r.get("rating", 5.0))
            
            is_suspicious = False
            # Check incentivized phrases
            if any(phrase in text for phrase in self.SUSPICIOUS_PHRASES):
                is_suspicious = True
            # Non-verified 5-star reviews with generic short text
            elif not verified and rating == 5.0 and len(text.split()) < 8:
                is_suspicious = True
                
            if is_suspicious:
                flagged_reviews_count += 1
            else:
                valid_reviews.append(r)
                
        if valid_reviews:
            valid_ratings = [float(r.get("rating", 5.0)) for r in valid_reviews]
            adjusted_avg = round(sum(valid_ratings) / len(valid_ratings), 2)
        else:
            adjusted_avg = round(raw_avg * 0.5, 2)
            
        authenticity_score = round(((len(reviews) - flagged_reviews_count) / max(1, len(reviews))) * 100.0, 1)
        
        # Rating Grade
        if authenticity_score >= 85.0:
            grade = "A_VERIFIED_TRUSTWORTHY"
        elif authenticity_score >= 65.0:
            grade = "B_MODERATE_PROMOTIONAL_NOISE"
        else:
            grade = "F_HIGH_SUSPICION_HIJACKED_REVIEWS"
            
        return {
            "sentinel": self.sentinel_name,
            "product_title": product_title,
            "total_reviews_audited": len(reviews),
            "flagged_untrustworthy_reviews": flagged_reviews_count,
            "authenticity_index": authenticity_score,
            "authenticity_grade": grade,
            "raw_average_rating": round(raw_avg, 2),
            "adjusted_authentic_rating": adjusted_avg,
            "verdict": "REVIEW_AUDIT_COMPLETED"
        }
