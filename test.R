require("RWeka")
training_data <- read.arff(file="/Users/chouclee/git/kddCup/train20Percent_new.arff")
#training_data <- read.arff(file="/Users/chouclee/git/kddCup/train.arff")
model <- J48(is_normal ~. -attack_type - , data = training_data)

# load testing data
#testing <- read.arff(file="/Users/chouclee/git/kddCup/test.arff")
#testing_data <- testing[1:41]
#testing_label <- testing[42]
test_without_newTypes <- read.arff(file="/Users/chouclee/git/kddCup/testWithoutNewAttackTypes_new.arff")
test_newTypes <- read.arff(file="/Users/chouclee/git/kddCup/testNewAttackTypes_new.arff")

## Use 10 fold cross-validation.
eval_model <- evaluate_Weka_classifier(model,
                                       numFolds = 10, complexity = FALSE,
                                       seed = 123, class = TRUE)
eval_model
# make predictions
prediction_without_newTypes <- predict(model, test_without_newTypes)
prediction_newTypes <- predict(model, test_newTypes)

# 
label = test_without_newTypes[43]
label = factor(label[[1]], levels = c("normal", "abnormal"))

# get confusion matrix
t <- table(prediction_without_newTypes, label) 
t

# calculate precision
precision = sum(diag(t))/length(label)
precision

# calculate precision of new type of attacks
#label = test_newTypes[42]
label = test_newTypes[43]
label = factor(label[[1]], levels = c("normal", "abnormal"))
newt <- table(prediction_newTypes, label)
newt

correct <- 0
for (i in seq_along(prediction_newTypes)) {
  if (prediction_newTypes[i] != "normal") {
    correct <- correct + 1
  }
}
precision_newTypes = correct/length(prediction_newTypes)
precision_newTypes

# calculate overal precision
overall_precision = (sum(diag(t)) + correct)/(length(prediction_without_newTypes) + 
                                                length(prediction_newTypes))
overall_precision
