import csv
import glob
    
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

def read_file_list(codes_list,path_string='/Volumes/spectro/FMRS2/LUBLIN/Dane/*/CODE/results_FIR/free_parameters.csv'):
    files=[]
    with open(codes_list, 'r') as file:
        for i, code in enumerate(file):
            files.extend(glob.glob(path_string.replace('CODE',code.rstrip())))
    return(files)


def cov_matrix_plot(files,indices,threshold=0.1):

    mean_est_values = []
    # Process remaining files
    for name in files:
        with open(name, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            column_data = [float(row[1]) for row in reader]
            mean_est_values.append([column_data[i] for i in indices])

    print(len(mean_est_values), len(mean_est_values[0]))



    mean_est_values_transposed = np.transpose(mean_est_values)
    covariance_matrix = np.cov(mean_est_values_transposed, rowvar=False)
    print(covariance_matrix.shape)

    # Plot covariance matrix
    fig, axs = plt.subplots(2, 1, figsize=(10, 8))

    # Plot matrix
    axs[0].imshow(covariance_matrix, cmap='hot', interpolation='nearest')
    axs[0].set_title('Covariance Matrix')
    fig.colorbar(axs[0].imshow(covariance_matrix, cmap='hot', interpolation='nearest'), ax=axs[0])

    # Plot standard plot
    axs[1].plot(covariance_matrix.mean(1))
    axs[1].set_title('average covariance')

    plt.tight_layout()
    plt.savefig('covariance_matrix.png',dpi=300)
    plt.show()

    outliers = [i for i, element in enumerate(covariance_matrix.mean(1)) if element > threshold]
    return outliers


def main():

    files=read_file_list(codes_list='3t_list.txt')
    print(files)

    # Get the index from the first file
    with open(files[0], 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        index = [row[0] for row in reader]

    indices = [i for i, element in enumerate(index) if element.endswith('_constant') or '_w' in element or '_b' in element]

    outliers=cov_matrix_plot(files,indices)
    print([files[i] for i in outliers])
    files = [files[i] for i in range(len(files)) if i not in outliers]
    outliers=cov_matrix_plot(files,indices,0.00045)
    print([files[i] for i in outliers])


if __name__ == "__main__":
    main()


