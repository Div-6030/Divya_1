from itertools import combinations

# Function to load transactions from the file
def load_data(filename):
    transactions = []
    with open(filename, 'r') as file:
        for line in file:
            transaction = set(line.strip().split(' '))
            transactions.append(transaction)
    return transactions

# Function to find frequent 1-itemsets
def find_frequent_1_itemsets(transactions, min_support_count):
    item_counts = {}
    for transaction in transactions:
        for item in transaction:
            if item in item_counts:
                item_counts[item] += 1
            else:
                item_counts[item] = 1

    # Filter items by min support
    frequent_itemsets = {frozenset([item]) for item, count in item_counts.items() if count >= min_support_count}
    return frequent_itemsets

# Function to generate candidate itemsets of size k
def generate_candidate_itemsets(prev_frequent_itemsets, k):
    candidates = set()
    itemsets = list(prev_frequent_itemsets)
    for i in range(len(itemsets)):
        for j in range(i + 1, len(itemsets)):
            candidate = itemsets[i].union(itemsets[j])
            if len(candidate) == k:
                candidates.add(candidate)
    return candidates

# Function to prune candidate itemsets by minimum support count
def prune_candidates(transactions, candidates, min_support_count):
    candidate_counts = {candidate: 0 for candidate in candidates}
    for transaction in transactions:
        for candidate in candidates:
            if candidate.issubset(transaction):
                candidate_counts[candidate] += 1

    # Filter candidates by support count
    frequent_itemsets = {candidate for candidate, count in candidate_counts.items() if count >= min_support_count}
    return frequent_itemsets

# Apriori algorithm
def apriori(filename, min_support_percent):
    transactions = load_data(filename)
    min_support_count = int((min_support_percent / 100) * len(transactions))

    # Find frequent 1-itemsets
    L1 = find_frequent_1_itemsets(transactions, min_support_count)
    Lk = L1
    k = 2

    # Store the overall frequent itemsets
    all_frequent_itemsets = L1

    # Iteratively find frequent itemsets of size k
    while Lk:
        print(f"Frequent itemsets of size {k-1}:")
        for itemset in Lk:
            print(f"{' '.join(itemset)}")

        # Generate candidates of size k
        Ck = generate_candidate_itemsets(Lk, k)

        # Prune candidates by minimum support
        Lk = prune_candidates(transactions, Ck, min_support_count)

        all_frequent_itemsets = all_frequent_itemsets.union(Lk)
        k += 1

    return all_frequent_itemsets

# Main function to execute the Apriori algorithm
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python myapriori.py <filename> <min_support_percentage>")
        sys.exit(1)

    filename = sys.argv[1]
    min_support_percent = float(sys.argv[2])

    apriori(filename, min_support_percent)
