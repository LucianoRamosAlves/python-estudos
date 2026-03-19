

com_vogal = input("digite  a sua palavra e veja quantas vogais")


sem_vogal = (
    com_vogal.count("a") +
    com_vogal.count("e") +
    com_vogal.count("i") +
    com_vogal.count("o") +
    com_vogal.count("u") 
)

print(sem_vogal)