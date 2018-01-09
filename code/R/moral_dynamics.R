# Load packages  ------------------------------------------------------------------------------
library(tidyjson)
library(magrittr)
library(corrr)
library(stringr)
library(svglite)
library(RSQLite)
library(tidyverse)

# EXP1: Read in and structure data ------------------------------------------------------------------
# con = dbConnect(SQLite(),dbname = "../javascript/experiment_1/participants.db");
con = dbConnect(SQLite(),dbname = "../../data/experiment1.db");
df.data = dbReadTable(con,"moral_dynamics")
dbDisconnect(con)

#filter out incompletes 
df.data = df.data %>% 
  filter(status %in% 3:5) %>% 
  filter(!str_detect(uniqueid,'debug')) %>% 
  filter(codeversion == 'experiment_1')

# demographic data 
df.demographics = df.data$datastring %>% 
  spread_values(condition = jnumber('condition'),
                age = jnumber('questiondata','age'),
                gender = jstring('questiondata','sex'),
                feedback = jstring('questiondata','feedback')
  ) %>% 
  rename(participant = document.id) %>% 
  mutate(time = difftime(df.data$endhit,df.data$beginhit,units = 'mins'))

# trial data 
df.long = df.data$datastring %>% 
  as.tbl_json() %>% 
  spread_values(participant = jstring('workerId')) %>%
  enter_object('data') %>%
  gather_array('order') %>% 
  enter_object('trialdata') %>% 
  gather_keys('index') %>% 
  append_values_string('values') %>% 
  as.data.frame() %>% 
  spread(index,values) %>% 
  mutate(clip = str_replace(clip,'video','')) %>% 
  mutate_at(vars(clip,rating),funs(as.numeric)) %>% 
  mutate(participant = factor(participant,labels = 1:length(unique(participant))) %>% as.character() %>% as.numeric) %>% 
  arrange(participant) %>% 
  select(-document.id)

# EXP1: Model predictions ---------------------------------------------------------------------------------------

#RMSE 
rmse = function(x,y){
  return(sqrt(mean((x-y)^2)))
}

df.predictions = read.csv("../../data/effort.csv",header=F) %>% 
  setNames(c("clip","prediction"))

df.tmp = df.long %>% 
  left_join(df.predictions) %>% 
  group_by(clip) %>% 
  summarise(data = mean(rating),
            effort = mean(prediction)) %>% 
  mutate(data = data/100) %>% 
  mutate(moving = ifelse(clip %in% c(4,12),0,1),
         # caused = ifelse(clip %in% c(12,21,22,25,26),0,1)) %$%
         caused = ifelse(clip %in% c(4,12,21,22,25,26),0,1)) %>%
  mutate(prediction.effort.causality = glm(data~effort+caused,data=.,family=binomial(link='logit'))$fitted.values,
         prediction.effort = glm(data~effort,data=.,family=binomial(link='logit'))$fitted.values)

df.long = df.long %>% 
  left_join(df.tmp %>% select(clip,prediction.effort.causality,prediction.effort))

df.tmp %>% 
  summarise(r.data.effort = cor(data,prediction.effort),
            rmse.data.effort = rmse(data*100,prediction.effort*100),
            r.data.effort.causality = cor(data,prediction.effort.causality),
            rmse.data.effort.causality = rmse(data*100,prediction.effort.causality*100)) %>% 
  mutate_all(funs(round(.,2)))

# EXP1: Plot results  -------------------------------------------------------------------------------

df.long %>% 
  # group_by(participant) %>%
  # mutate(rating = scale(rating)) %>%
  # ungroup() %>%
  ggplot(aes(x=clip,y=rating))+
  stat_summary(fun.data = mean_cl_boot, geom = 'linerange', size = 0.5)+
  stat_summary(fun.y = mean, geom = 'line', size = 1)+
  stat_summary(fun.y = mean, geom = 'point', size = 2)+
  geom_point(alpha = 0.2, position = position_jitter(width = 0.1, height = 0))+
  geom_line(aes(x=clip,y=prediction.effort*100),color='red',size=2,alpha=0.5)+
  geom_point(aes(x=clip,y=prediction.effort*100),color='red',size=2,alpha=0.5)+
  geom_line(aes(x=clip,y=prediction.effort.causality*100),color='blue',size=2,alpha=0.5)+
  geom_point(aes(x=clip,y=prediction.effort.causality*100),color='blue',size=2,alpha=0.5)+
  # geom_line(aes(group=participant),size=0.5,alpha=0.2)+
  labs(y = 'Badness rating', x = 'clip number')+
  scale_x_continuous(breaks = 1:28,labels = 1:28)+
  theme_bw()+
  theme(text = element_text(size = 20),
    panel.grid = element_blank(),
    legend.position='bottom')
  # ggsave("../../figures/plots/mean_judgments.pdf",width=12,height=4)
  # ggsave("../../figures/plots/mean_judgments_predictions.pdf",width=12,height=4)
  # ggsave("../../figures/plots/mean_judgments_predictions.png",width=12,height=4)
  # ggsave("../../figures/plots/mean_judgments_predictions.svg",width=12,height=4)

# EXP2: Read in and structure data ------------------------------------------------------------------

# con = dbConnect(SQLite(),dbname = "../javascript/experiment_1/participants.db");
con = dbConnect(SQLite(),dbname = "../../data/experiment2.db");
df.data = dbReadTable(con,"moral_dynamics")
dbDisconnect(con)

#filter out incompletes 
df.data = df.data %>% 
  filter(status %in% 3:5) %>% 
  filter(!str_detect(uniqueid,'debug')) %>% 
  filter(codeversion == 'experiment_2')

# demographic data 
df.demographics = df.data$datastring %>% 
  spread_values(condition = jnumber('condition'),
                age = jnumber('questiondata','age'),
                gender = jstring('questiondata','sex'),
                feedback = jstring('questiondata','feedback')
  ) %>% 
  rename(participant = document.id) %>% 
  mutate(time = difftime(df.data$endhit,df.data$beginhit,units = 'mins'))

# trial data 
df.long = df.data$datastring %>% 
  as.tbl_json() %>% 
  spread_values(participant = jstring('workerId')) %>%
  enter_object('data') %>%
  gather_array('order') %>%
  enter_object('trialdata') %>% 
  spread_values(display = jstring('order'),
                rating = jnumber('rating')) %>%
  enter_object('clip') %>% 
  gather_array('index') %>%
  append_values_string('name') %>% 
  as.data.frame() %>% 
  select(-document.id) %>% 
  spread(index,name) %>% 
  mutate(clips = paste(`1`,`2`,sep="_")) %>% 
  mutate(rating = ifelse(display == 'flipped',100-rating,rating)) %>%
  mutate(clips = str_replace_all(clips,"video","")) %>% 
  mutate(rating = rating-50) %>% 
  select(-c(display,`1`,`2`)) %>% 
  mutate(participant = factor(participant,labels = 1:length(unique(participant))))

# results from moral kinematics paper
df.kinematics = read.csv("../../data/moral_kinematics_results.csv",stringsAsFactors = F)

# EXP2: Model predictions  --------------------------------------------------------------------

df.predictions = read.csv("../../data/effort.csv",header=F) %>% 
  setNames(c("clip","prediction")) %>% 
  mutate(caused = ifelse(clip %in% c(4,12,21,22,25,26),0,1))

df.predictions = df.long$clips %>% 
  unique() %>% 
  str_split("_") %>% 
  unlist() %>% 
  as.numeric() %>% 
  matrix(ncol=2,byrow=T) %>% 
  as.data.frame() %>% 
  setNames(c('clip1','clip2')) %>% 
  mutate(effort1 = df.predictions$prediction[clip1],
         effort2 = df.predictions$prediction[clip2],
         caused1 = df.predictions$caused[clip1],
         caused2 = df.predictions$caused[clip2],
         # diff.effort = effort2/effort1,
         diff.effort = effort2-effort1,
         diff.causality = caused2-caused1,
         clips = paste(clip1,clip2,sep="_")) %>% 
  select(clips,diff.effort,diff.causality)

df.regression = df.long %>% 
  group_by(clips) %>% 
  summarise(mean = mean(rating)) %>% 
  left_join(df.predictions) %>% 
  mutate(model.effort = lm(mean~diff.effort,data=.)$fitted.values,
         model.effort.causality = lm(mean~diff.effort+diff.causality,data=.)$fitted.values)


# EXP2: Plot - Means  -------------------------------------------------------------------------------

df.long %>% 
  # group_by(participant) %>%
  # # mutate(rating = scale(rating)) %>%
  # ungroup %>% 
  ggplot(aes(x=clips,y=rating))+
  geom_hline(yintercept = 0, linetype = 2, color = 'gray')+
  stat_summary(fun.data = mean_cl_boot, geom = 'linerange', size = 0.5)+
  stat_summary(fun.y = mean, geom = 'point', size = 3)+
  geom_point(alpha = 0.2, position = position_jitter(width = 0.1, height = 0))+
  geom_point(data = df.regression,aes(x=clips,y=model.effort),color='red',size=3,alpha=1)+
  geom_point(data = df.regression,aes(x=clips,y=model.effort.causality),color='green',size=3,alpha=1)+
  # geom_line(aes(group=participant),size=0.5,alpha=0.2)+
  labs(y = 'Which action was worse?\n(1st clip vs. 2nd clip)', x = 'clips')+
  theme_bw()+
  theme(text = element_text(size = 20),
        panel.grid = element_blank(),
        legend.position='bottom')
# ggsave("../../figures/plots/exp2_judgments.pdf",width=10,height=4)
# ggsave("../../figures/plots/exp2_judgments.pdf",width=10,height=6)
# ggsave("../../figures/plots/mean_judgments_predictions.pdf",width=12,height=4)
# ggsave("../../figures/plots/mean_judgments_predictions.png",width=12,height=4)
# ggsave("../../figures/plots/mean_judgments_predictions.svg",width=12,height=4)

# EXP2: Plot - Scatter ------------------------------------------------------------------------

df.regression %>% 
  ggplot(aes(x=mean,y=model.effort))+
  # stat_summary(y)+
  geom_point()

df.regression %$% 
  cor(mean,model.effort)
  
# EXP2: Plot - Bar plot (comparison with kinematics paper results) ------------------------------------------------------------------------

df.long %>% 
  group_by(clips) %>% 
  summarise(proportion = sum(rating<0)/n()) %>% 
  left_join(df.kinematics %>% filter(clips != 'N/a')) %>% 
  select(-trial) %>% 
  gather(index,value,-clips) %>% 
  mutate(index = factor(index,levels = c('rating','proportion'),labels = c('original','replication'))) %>% 
  ggplot(aes(x = clips, y = value, group = index,fill = index))+
  geom_bar(stat='identity', position = position_dodge(0.9),color = 'black',width=0.9)+
  geom_hline(yintercept = 0.5,linetype=2,size=1)+
  scale_fill_brewer(type='qual',palette=3)+
  theme_bw()+
  labs(y = '% first clip worse', fill = '')+
  theme(panel.grid = element_blank(),
        legend.position = 'top',
        text = element_text(size=20))+
  ggsave("../../figures/plots/exp2_proportions.pdf",width=12,height=4)

  
# df.long %>% 
#   group_by(clips) %>% 
#   summarise(proportion = sum(rating<0)/n()) %>% 
#   left_join(df.kinematics %>% filter(clips != 'N/a')) %$% 
#   cor(proportion,rating)

