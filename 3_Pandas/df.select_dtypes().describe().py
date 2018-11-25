train_df.select_dtypes('object').describe()

train_df.select_dtypes(exclude=('object')).describe().boxplot(figsize=(20,8))
train_df.select_dtypes(exclude=('object')).describe()
