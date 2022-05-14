from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
from typing import Dict, List, Tuple
from colorama import Fore, Style
import json


class Neo:
    def __init__(self, uri, user, password):
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            print(Fore.GREEN+"Successfully connected to Neo4J"+Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED+"Error : {e}"+Style.RESET_ALL)
            raise Exception("Failed to connect to database")

    def create_roles(self, roles, orgId):
        try:
            with self.driver.session() as session:
                for role in roles:
                    session.write_transaction(
                        self._create_role, role, orgId
                    )
            print(Fore.GREEN+"Successfully created roles"+Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED+f"Error : {e}"+Style.RESET_ALL)
            raise Exception("DB Error")

    @staticmethod
    def _create_role(tx, role, orgId):
        try : 
            query = '''
                    CREATE (r: ROLE {name : $role, orgId : $orgId})
                '''
            tx.run(query, role=role, orgId=orgId)
        except Exception as e:
            print(Fore.RED+f"Error : {e}"+Style.RESET_ALL)
            raise Exception("DB Transaction Error")
    
    def delete_roles(self, orgId):
        try:
            with self.driver.session() as session:
                session.write_transaction(
                    self._delete_roles, orgId
                )
            print(Fore.GREEN+"Successfully deleted roles"+Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED+f"Error : {e}"+Style.RESET_ALL)
            raise Exception("DB Error")

    @staticmethod
    def _delete_roles(tx, orgId):
        try : 
            query = '''
                    MATCH (r: ROLE {orgId : $orgId}) DELETE r
                '''
            tx.run(query, orgId=orgId)
        except Exception as e:
            print(Fore.RED+f"Error : {e}"+Style.RESET_ALL)
            raise Exception("DB Transaction Error")
            
    def close(self):
        self.driver.close()


def get_roles_and_triples(fname: str) -> Tuple[List, List[Tuple[str, str, str]]]:
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
        return list(roles.values()), res
    except Exception as e:
        print(Fore.RED + f"Error : {e}" + Style.RESET_ALL)
        return [], []


def get_credentials(fname: str) -> Dict:
    try:
        f = dict(json.load(open(fname, "r")))
        required_fields = ["uri", "user", "password"]
        for r in required_fields:
            if not r in f:
                raise Exception(f"No feild \'{r}\' found in file")
        print(Fore.GREEN + "Scanned credentials successfully" + Style.RESET_ALL)
        return f
    except Exception as e:
        print(Fore.RED + f"Error : {e}" + Style.RESET_ALL)
        raise Exception("Invalid credentials file")


def main() -> None:
    try:
        roles, triples = get_roles_and_triples("relationships.json")
        credentials = get_credentials("secrets.json")
        n = Neo(
            credentials["uri"],
            credentials["user"],
            credentials["password"]
        )
        n.create_roles(roles, 1)
        n.create_roles(roles, 2)
        # n.delete_roles(1)
        # n.delete_roles(1)
        n.close()
        print(Fore.GREEN + "Created Graph in Aura DB successfully" + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"Error : {e}" + Style.RESET_ALL)


if __name__ == "__main__":
    main()
