from typing import List, Tuple
from rdflib import Graph, Literal
from colorama import Fore, Style
import json


def get_triples(fname: str) -> List[Tuple[str, str, str]]:

    try:
        f = json.load(open(fname, "r"))
        rel_map = f["map"]
        roles = f["roles"]
        res = []

        for t in f["triples"]:
            res.append(
                (
                    roles[t["subject"]],
                    rel_map[t["predicate"]],
                    roles[t["object"]],
                )
            )

        print(Fore.GREEN + "Scanned json successfully" + Style.RESET_ALL)
        return res

    except Exception as e:
        print(Fore.RED + f"Error : {e}" + Style.RESET_ALL)
        return []


def main() -> None:
    
    try : 
        g = Graph()
        tuples = get_triples("relationships.json")
        for s, p, o in tuples : 
            g.add((Literal(s), Literal(p), Literal(o)))
        g.serialize(destination="result.ttl", format="ttl")    
        
        print(Fore.GREEN + "Created Graph successfully" + Style.RESET_ALL)
    
    except Exception as e:
        print(Fore.RED + f"Error : {e}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
