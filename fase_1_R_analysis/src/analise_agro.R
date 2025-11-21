# YanPimentelCotta_RM562836_fase2_cap7

# Definir o caminho do arquivo CSV relativo ao diretório do script
arquivo_csv <- file.path("..", "data", "agro_data.csv")

# Verificar se o arquivo existe
if (!file.exists(arquivo_csv)) {
  stop("Erro: O arquivo 'agro_data.csv' não foi encontrado em: ", arquivo_csv)
}

# Carregar a base de dados (usando read.csv2 para separador ';')
dados <- read.csv2(arquivo_csv)

# Imprimir nomes das colunas para depuração
cat("Nomes das colunas no CSV:\n")
print(colnames(dados))

# Verificar se a coluna existe
if (!"Producao..toneladas." %in% colnames(dados)) {
  stop("Erro: A coluna 'Producao..toneladas.' não foi encontrada. Colunas disponíveis: ", paste(colnames(dados), collapse = ", "))
}

# Análise Exploratória da Variável Quantitativa: Produção (toneladas)
producao <- dados$"Producao..toneladas."

# Medidas de Tendência Central
media <- mean(producao)
mediana <- median(producao)
moda <- names(sort(table(producao), decreasing = TRUE))[1]

# Medidas de Dispersão
variancia <- var(producao)
desvio_padrao <- sd(producao)
amplitude <- max(producao) - min(producao)

# Medidas Separatrizes
quartis <- quantile(producao, probs = c(0.25, 0.5, 0.75))
decis <- quantile(producao, probs = seq(0.1, 0.9, by = 0.1))

# Análise Gráfica Quantitativa
# Definir caminho para a pasta docs
pasta_docs <- file.path("..", "docs")

# Verificar se a pasta docs existe
if (!dir.exists(pasta_docs)) {
  dir.create(pasta_docs)
}

# Salvar histograma
png(file.path(pasta_docs, "histograma_producao.png"))
hist(producao, main = "Histograma da Produção de Soja", xlab = "Produção (toneladas)", col = "lightblue")
dev.off()

# Salvar boxplot
png(file.path(pasta_docs, "boxplot_producao.png"))
boxplot(producao, main = "Boxplot da Produção de Soja", ylab = "Produção (toneladas)")
dev.off()

# Imprimir resultados
cat("Medidas de Tendência Central:\n")
cat("Média:", media, "\n")
cat("Mediana:", mediana, "\n")
cat("Moda:", moda, "\n\n")

cat("Medidas de Dispersão:\n")
cat("Variância:", variancia, "\n")
cat("Desvio Padrão:", desvio_padrao, "\n")
cat("Amplitude:", amplitude, "\n\n")

cat("Medidas Separatrizes:\n")
cat("Quartis:\n")
print(quartis)
cat("Decis:\n")
print(decis)

# Análise Gráfica da Variável Qualitativa: Classificação de Produtividade
# Verificar se a coluna existe
if (!"Classificacao.de.Produtividade" %in% colnames(dados)) {
  stop("Erro: A coluna 'Classificacao.de.Produtividade' não foi encontrada. Colunas disponíveis: ", paste(colnames(dados), collapse = ", "))
}

classificacao <- dados$"Classificacao.de.Produtividade"
tabela_freq <- table(classificacao)

# Salvar gráfico de barras
png(file.path(pasta_docs, "grafico_classificacao.png"))
barplot(tabela_freq, main = "Distribuição da Classificação de Produtividade", 
        xlab = "Classificação", ylab = "Frequência", col = "lightgreen")
dev.off()