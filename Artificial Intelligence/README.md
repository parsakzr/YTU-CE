# A1 - Genetik Algoritması ile İkili metin sınıflandırma

* Parsa Kazerooni - 19011915
* Hümeysa Şimşek - 19011506

## Kullanılan Veriseti

[Sentiment Labelled Sentences][https://archive.ics.uci.edu/ml/datasets/Sentiment+Labelled+Sentences](1) imdb, amazon ve yelp'teki yorumlarından oluşan pozitif/negatif  metin sınıflandırma UCI verisetidir. her farkli kaynak için, 500 tane negatif ve 500 tane pozitif örnek mevcüttür. Toplamda 3000 yorumu içerir.

## Genetik Algoritması

Her bir birey, N farklı Kelimeden oluşturulur. ilk N/2 kelime pozitif sınıfa, ve son N/2 kelime, negatif sınıfına aittir.

Fitness değerini hesaplamak için, her bir cümlenin kelimelerinden, hangileri pozitif sınıfına ve hangileri negatif sınıfına ait olduğunu sayarız. daha fazla kelime içeren sınıf, metnin algoritma tarafından tahmini sınıfı olacak. Doğru tahminler oranı, fitness değeri olarak hesaplanır.

```py
def fitness(individual, train_set):
    count_c1, count_c0 = 0, 0
    count_correct_prediction = 0
    for line in train_set:
        line, label = line["text"], line["label"]
        for word in line.split():
            if word in individual[:len(individual)//2]:
                count_c1 += 1
            elif word in individual[len(individual)//2:]:
                count_c0 += 1
    
        prediction = 1 if count_c1 >= count_c0 else 0
        if prediction == label: # if the prediction is correct
            count_correct_prediction += 1
    return count_correct_prediction / len(train_set)
```

sonra her bir jenerasyon için birçok birey, fitness değerlerine göre sıralanacaklar, elite olan bireyler arasında, crossover ve mutation yaptırarak sonraki jenerasyonu oluştururuz.

Algoritmanın kodu bu şeklindedir:

```py
def geneticAlgorithm(train_set, population_size, individual_size, mutation_rate, elitism_rate= 0.2, max_generations=1000, verbose=True):
    # Genetic Algorithm

    
    population = [newIndividual(words, size=individual_size) for _ in range(population_size)]
    
    population = sorted(population, key=lambda individual: fitness(individual, train_set), reverse=True)
    
    best_individual = population[0]
    
    best_fitness = [fitness(best_individual, train_set)]
    
    avg_fitness = [sum([fitness(individual, train_set) for individual in population]) / population_size]
    
    num_generation = 0
    while num_generation < max_generations:
        
        next_generation = []
        
        next_generation.extend(population[:int(elitism_rate * population_size)])
        
        while len(next_generation) < population_size:
            
            parent1, parent2 = random.choices(population, k=2)
            
            child = crossover(parent1, parent2)
            
            child = mutate(child, words, mutation_rate)
            
            next_generation.append(child)
        
        next_generation = sorted(next_generation, key=lambda individual: fitness(individual, train_set), reverse=True)
        
        population = next_generation
        
        if fitness(population[0], train_set) > fitness(best_individual, train_set):
            best_individual = population[0]
        
        best_fitness.append(fitness(best_individual, train_set))
        
        avg_fitness.append(sum([fitness(individual, train_set) for individual in population]) / population_size)
        

        if verbose==True and (num_generation % ( max_generations // 10) == 0) :
            print(f"Gen {num_generation+1}: Best fitness = {best_fitness[-1]}, Avg fitness = {avg_fitness[-1]}")
            print(f"Best individual = {best_individual}")

        num_generation += 1
```

## Referanslar

[1] 'From Group to Individual Labels using Deep Features', Kotzias et. al,. KDD 2015.
