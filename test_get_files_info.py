# 1. On importe la fonction depuis le dossier 'functions'
from functions.get_files_info import get_files_info

# 2. Premier test : le dossier courant dans "calculator"
print("Result for current directory:")
resultat = get_files_info("calculator", ".")
print(resultat)

print("Result for 'pkg' directory:")
resultat = get_files_info("calculator", "pkg")
print(resultat)

print("Result for '/bin' directory:")
resultat = get_files_info("calculator", "/bin")
print(resultat)

print("Result for '../' directory:")
resultat = get_files_info("calculator", "../")
print(resultat)
