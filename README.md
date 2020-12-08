# eastmoney

#### 介绍
股吧数据分析系统，对股吧数据进行分析预测与股票走势相关性
三部分组成
1.爬虫组件
2.数据分析组件
3.WEB后台数据管理组件


#### 软件架构
本系统使用python作为开发语言、MYSQL作为数据存储系统、pandas 科学计算包进行分析处理
######
一、爬虫组件  
   1.通过此url:http://guba.eastmoney.com/remenba.aspx?type=1&tab=2  首先获取股票代码
   2.获取到的股票代码插入MYSQL数据库表中，生成一张初始化任务表
   3.启用多进程，多线程，获取任务，对每只股票抓取，抓取地址：https://mguba.eastmoney.com/interface/GetData.aspx， 此url是POST请求
   4.进行多次翻页，直到抓取到全部所需数据为止，
   5.经过数据处理过滤引擎，过滤掉无用数据，如新闻公告等信息，对文章数据进行情感评分（分值0-1， 数字越大代表越正面）使用SnowNLP库
   6.抓取的指标参数有：点赞数、评论数、阅读数、转发数、文本内容、文本标题、用户信息、用户影响力、发布时间、更新时间，以及计算得到的情感评分

######
二、数据分析组件  
   1.初始化一张数据分析任务表
   2.以此对每只股票进行日分析统计
   3.统计维度，情感评分划分数据，0~0.5 为负面， 0.5~1是正面，计算维度分值，负面（0.5-情感评分） * 2， 正面（1-情感评分）* 2
   4.分别对每只股票按照日统计正负面汇总汇总 分值为 = （20%用户影响力+20%帖子点击数+20%点赞数+30%回帖数+10%转发） * 正负面评分
   相应sql语句
   ```
   select
	DATE_FORMAT(publish_time, '%Y-%m-%d') AS dt, count(1) total_count,
	SUM(case when a.score > 0.5 then 1 else 0 END) good_count,
	SUM(case when a.score >= 0.5 then (a.score - 0.5) * 2 * (a.user_influ_level * 0.2 + a.click_count * 0.2 + a.like_count * 0.2 + a.comment_count * 0.3 + a.forward_count * 0.1)  else 0 END) good_score,
    SUM(case when a.score < 0.5 then (0.5 - a.score) * 2 * (a.user_influ_level * 0.2 + a.click_count * 0.2 + a.like_count * 0.2 + a.comment_count * 0.3 + a.forward_count * 0.1) else 0 END) bad_score
    from guba_info a where symbol_id={0} GROUP BY dt
   ```
   5.在每只股票汇总的基础上进行，沪市300汇总、中证500汇总， 中证1000汇总，全A股汇总，医药板块汇总

######  
三、web 后台数据管理
    1.使用Django admin框架搭建的管理后台
    2.后台数据主要有 成分股数据、股票资产信息、股吧统计信息，三大核心模块组成
    3.后台提供了数据校验、参考依据



