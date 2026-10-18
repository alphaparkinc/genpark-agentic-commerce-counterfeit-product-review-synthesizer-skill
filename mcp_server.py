#!/usr/bin/env python3
import json
import sys
from client import AgenticCommerceReviewAuthenticitySentinel

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sentinel = AgenticCommerceReviewAuthenticitySentinel()
        revs = [
            {"rating": 5, "text": "Received this product for free in exchange for honest review", "verified_purchase": False},
            {"rating": 5, "text": "Best purchase ever five stars", "verified_purchase": False},
            {"rating": 3, "text": "Battery life lasts about 4 hours, build quality is acceptable.", "verified_purchase": True}
        ]
        res = sentinel.audit_product_reviews("Wireless Earbuds X", revs)
        assert res["flagged_untrustworthy_reviews"] == 2
        assert res["adjusted_authentic_rating"] == 3.0
        print(f"[TEST PASS] Review Authenticity Grade: {res['authenticity_grade']}")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-review-guard", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "audit_product_reviews", "description": "Audit product reviews and calculate authentic rating"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                sentinel = AgenticCommerceReviewAuthenticitySentinel()
                out = sentinel.audit_product_reviews(args.get("product_title", "Product"), args.get("reviews", []))
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
