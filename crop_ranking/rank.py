# Uses ELO/pagerank to rank crops.  Alternative methods:  Borda Count, Bradley-Terry Model
import networkx as nx

# Sample data: List of rankings (ordered lists of 5 items)
rankings = [
    ['item1', 'item2', 'item3', 'item4', 'item5'],
    ['item3', 'item2', 'item5', 'item1', 'item4'],
    # ... (add as many rankings as you have)
]


def rank(rankings):
    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes
    items = set(item for ranking in rankings for item in ranking)
    G.add_nodes_from(items)

    # Add edges based on rankings
    for ranking in rankings:
        for i in range(len(ranking)):
            for j in range(i + 1, len(ranking)):
                higher = ranking[i]
                lower = ranking[j]
                if G.has_edge(higher, lower):
                    G[higher][lower]['weight'] += 1
                else:
                    G.add_edge(higher, lower, weight=1)

    # Compute PageRank
    pr = nx.pagerank(G, alpha=0.85, weight='weight')

    # Sort items by PageRank score
    sorted_items = sorted(pr.items(), key=lambda x: x[1], reverse=True)

    # Output the final ranking
    print("Final Ranking based on PageRank:")
    for rank, (item, score) in enumerate(sorted_items, start=1):
        print(f"{rank}. {item} (Score: {score:.6f})")

    return sorted_items
