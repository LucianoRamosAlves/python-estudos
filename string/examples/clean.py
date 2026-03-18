sujo = "9184-Isabel, ( D@t@ Engineer ) ;; 75 anos   "


limpo = (
sujo
.replace("9184", "Nome:")
.replace(",", " ")
.replace(";", "")
.replace("(", "|")
.replace("-", " ")
.replace(")", "|")
.replace("@", "a")
)

print(limpo.strip()) 