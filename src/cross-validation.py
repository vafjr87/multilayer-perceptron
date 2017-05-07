import os
import perceptron
import argparse

def classes(path):
	"""
	Listagem das classes existentes no diretório
	:Parameters:
		path: diretório de trabalho
	"""
	classes = list()

	for f in os.listdir(path):
		if f[:8] not in classes:
			classes.append(f[:8])

	return classes

def dataset(classes):
	"""
	Reúne os arquivos de cada classe em uma lista de listas
	:Parameters:
		classes: cada uma das classes a ser buscada
	"""
	dataset = list()

	for i in range(len(classes)):
		files = [f for f in os.listdir(path) if f.startswith(classes[i])]
		dataset.append(files)

	return dataset

def kfold(dataset, hidden_neurons, alpha, classes_num, descriptor, path, epochs, descriptor_param1, descriptor_param2, descriptor_param3 = 0):
	"""
	Validação cruzada utilizando o mé todo k-fold
	:Parameters:
		training: lista de imagens contidas em classes (cada classe é uma lista)
	"""

	# Define número de folds e tamanho do subset (que sempre vai ser igualmente dividido entre as classes)
	num_folds = 5
	subset_size = int(len(dataset[0])/num_folds)	

	for fold_i in range(num_folds): 
		testing_this_round = list()
		training_this_round = list()
		
		for dataset_j in range(len(dataset)):
			testing_this_round = testing_this_round + dataset[dataset_j][fold_i*subset_size:][:subset_size]      
			training_this_round = training_this_round + dataset[dataset_j][:fold_i*subset_size] + dataset[dataset_j][(fold_i+1)*subset_size:]
		

		mlp = perceptron.MLP(hidden_neurons, alpha, classes_num, descriptor, path, epochs, descriptor_param1, descriptor_param2, descriptor_param3)
		mlp.run(training_this_round, testing_this_round, fold_i)

if __name__ == "__main__":	
	# Definição do diretório de trabalho
	path = './data/dataset1/treinamento/'
	classes = classes(path)
	dataset = dataset(classes)

	parser = argparse.ArgumentParser(description='Choice of which image descriptor will be used in the MLP') 
	parser.add_argument('--descriptor', '--desc', required= True, help="Choose descriptor HOG or LBP to use in the MLP")
	args = parser.parse_args()
	descriptor = args.descriptor

	epochs = 1
	hidden_neurons = 32
	alpha = 1.0

	hog_orientations = 9
	hog_pixels_per_cell = 8
	hog_cells_per_block = 1
	lbp_points = 8
	lbp_radius = 2

	if descriptor in ['HOG', 'LBP']:
		if descriptor == 'HOG':
			kfold(dataset, hidden_neurons, alpha, len(classes), descriptor, path, epochs, hog_orientations, hog_pixels_per_cell, hog_cells_per_block)
		elif descriptor == 'LBP':
			kfold(dataset, hidden_neurons, alpha, len(classes), descriptor, path, epochs, lbp_points, lbp_radius)
	else:
		print("The descriptor should be 'HOG' or 'LBP'")