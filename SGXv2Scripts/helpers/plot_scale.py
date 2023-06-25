import csv

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import commons


def readable_names(x, str=None):
    modifier = "(" + str + ")" if str is not None else ""
    if "native" in x:
        return 'Plain CPU' + " " + modifier
    elif 'sgx' in x:
        return 'SGX Data in Enclave' + " " + modifier


def plot_threads():
    df_native = pd.read_csv("../data/scale-threads-native-output.csv")
    df_sgx = pd.read_csv("../data/scale-threads-sgx-output.csv")

    # df_native['slowdown'] = df_sgx['throughput'] / df_native['throughput']
    for alg in df_native['alg'].unique():
        df_sgx_temp = df_sgx[df_sgx['alg'] == alg]
        df_native_temp = df_native[df_native['alg'] == alg]
        base_sgx = df_sgx_temp[df_sgx_temp['threads'] == 1]['throughput'].values[0]
        base_native = df_native_temp[df_native_temp['threads'] == 1]['throughput'].values[0]
        var_sgx = []
        var_native = []
        for th in [1, 2, 4, 8, 16,32]:
            var_sgx.append(df_sgx_temp[df_sgx_temp['threads'] == th]['throughput'].values[0] / base_sgx)
            var_native.append(df_native_temp[df_native_temp['threads'] == th]['throughput'].values[0] / base_native)
        df_sgx_temp = df_sgx_temp.reset_index()
        df_native_temp = df_native_temp.reset_index()
        df_sgx_temp['speedup'] = pd.Series(var_sgx)
        df_native_temp['speedup'] = pd.Series(var_native)
        df_joined = pd.concat([df_native_temp,df_sgx_temp], ignore_index=True)
        df_joined['mode'] = df_joined['mode'].apply(lambda x: readable_names(x))
        g = sns.barplot(data=df_joined, x='threads', y='speedup', hue='mode')
        g.set(title=alg)
        plt.show()


def plot_two_in_one(algname1, algname2):
    df_native = pd.read_csv("../data/scale-r-native-output_correct.csv")
    df_sgx = pd.read_csv("../data/scale-r-sgx-preload-output_correct.csv")
    s_sizes = [1, 20, 28, 512]
    df_native_temp = df_native[df_native['alg'].isin([algname1, algname2])]
    df_sgx_temp = df_sgx[df_sgx['alg'].isin([algname1, algname2])]
    df_joined = pd.concat([df_native_temp, df_sgx_temp], ignore_index=True)
    df_joined['mode'] = df_joined['mode'].apply(lambda x: readable_names(x))
    g = sns.relplot(kind='line', data=df_joined, x='sizeS', y='throughput', hue='mode', style='alg', col='sizeR',
                    marker='o', aspect=0.5)
    g.set(ylim=(0, None))
    # g.set(yscale="log")
    for ax in g.axes.flat:
        ax.set_xticks(ticks=range(500, 2500 + 1, 500))
    g.set(xlabel='Size of Inner Table [MB]', ylabel='Throughput [M rec/s]')
    g.set_titles(col_template='Size of Outer Table: {col_name} [MB]')
    g._legend.set_title(None)
    # plt.show()
    plt.savefig('../img/scale_' + algname1 + '_' + algname2 + '.pdf')


def plot():
    df_native = pd.read_csv("../data/scale-r-native-output_correct.csv")
    df_sgx = pd.read_csv("../data/scale-r-sgx-preload-output_correct.csv")
    s_sizes = [1, 20, 28, 512]
    algos = df_native['alg'].unique()
    for alg in algos:
        df_native_temp = df_native[df_native['alg'] == alg]
        df_sgx_temp = df_sgx[df_sgx['alg'] == alg]
        df_joined = pd.concat([df_native_temp, df_sgx_temp], ignore_index=True)
        df_joined['mode'] = df_joined['mode'].apply(lambda x: readable_names(x))
        g = sns.relplot(kind='line', data=df_joined, x='sizeS', y='throughput', hue='mode', col='sizeR', marker='o',
                        aspect=0.5)
        g.set(ylim=(0, None))
        for ax in g.axes.flat:
            ax.set_xticks(ticks=range(500, 2500 + 1, 500))
        g.set(xlabel='Size of Inner Table [MB]', ylabel='Throughput [M rec/s]', title=alg)
        g.set_titles(col_template='Size of Outer Table: {col_name} [MB]')
        g._legend.set_title(None)
        plt.savefig('../img/scale_' + alg + '.pdf')


def plot_swapped():
    df_native = pd.read_csv("../data/scale-native-output_swapped.csv")
    df_sgx = pd.read_csv("../data/scale-sgx-output_swapped.csv")
    s_sizes = [1, 20, 28, 512]
    algos = df_native['alg'].unique()
    for alg in ['INL']:
        df_native_temp = df_native[df_native['alg'] == alg]
        df_sgx_temp = df_sgx[df_sgx['alg'] == alg]
        df_joined = pd.concat([df_native_temp, df_sgx_temp], ignore_index=True)
        df_joined['mode'] = df_joined['mode'].apply(lambda x: readable_names(x))
        g = sns.relplot(kind='line', data=df_joined, x='sizeR', y='throughput', hue='mode', col='sizeS', marker='o',
                        aspect=0.5)
        g.set(ylim=(0, None))
        for ax in g.axes.flat:
            ax.set_xticks(ticks=range(500, 2500 + 1, 500))
        g.set(xlabel='Size of Outer Table [MB]', ylabel='Throughput [M rec/s]', title=alg)
        g.set_titles(col_template='Size of Inner Table: {col_name} [MB]')
        g._legend.set_title(None)
        plt.savefig('../img/scale_swapped_' + alg + '.pdf')


def plot_overview():
    df_native = pd.read_csv("../data/scale-r-native-output_correct.csv")
    df_sgx = pd.read_csv("../data/scale-r-sgx-preload-output_correct.csv")
    df_joined = pd.concat([df_native, df_sgx], ignore_index=True)
    df_joined = df_joined[(df_joined['sizeR'] == 512) & (df_joined['sizeS'] == 2500)]
    df_joined['mode'] = df_joined['mode'].apply(lambda x: readable_names(x))
    g = sns.barplot(data=df_joined, x='alg', y='throughput', hue='mode',
                    order=['INL', 'CHT', 'PHT', 'RHT', 'RHO', 'RSM', 'PSM', 'MWAY'])
    g.set(xlabel='Algorithms', ylabel='Throughput [M rec/s]')
    for c in g.containers:
        l = [f'{(v.get_height()):.0f}' for v in c]
        g.bar_label(c, labels=l, label_type='edge')
    plt.savefig('../img/join_overview.pdf')


if __name__ == '__main__':
    #plot_overview()
    plot_threads()
    # plot_threads()
    #plot()
    #plot_swapped()
    #plot_two_in_one('CHT', 'PHT')
    #plot_two_in_one('RHO', 'RHT')
    #plot_two_in_one('MWAY', 'PSM')
