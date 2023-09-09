package com.phone.Scheduled;

import com.phone.dao.CronDao;
import com.phone.service.CronService;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.SchedulingConfigurer;
import org.springframework.scheduling.config.ScheduledTaskRegistrar;
import org.springframework.scheduling.support.CronTrigger;
import org.springframework.util.StringUtils;

import java.time.LocalDateTime;

/**
 * 动态定时任务配置类
 * @author pan_junbiao
 **/
@Configuration      //1.主要用于标记配置类，兼备Component的效果
@EnableScheduling   //2.开启定时任务
public class DynamicScheduleConfigurer implements SchedulingConfigurer
{


    //注入mapper
    @Autowired
    @SuppressWarnings("all")
    CronService cronService;

    @Autowired
    Task task;
    /**
     * 执行定时任务.
     */
    @Override
    public void configureTasks(ScheduledTaskRegistrar taskRegistrar)
    {
        taskRegistrar.addTriggerTask(
                //1.添加任务内容(Runnable)
                  task,
//                () -> System.out.println("欢迎访问 pan_junbiao的博客: " + LocalDateTime.now().toLocalTime()),


                //2.设置执行周期(Trigger)
                triggerContext -> {
                    //2.1 从数据库获取执行周期
                    String cron = cronService.getCron();
                    //2.2 合法性校验.
                    if (StringUtils.isEmpty(cron)) {
                        // Omitted Code ..
                    }
                    if (cron!=null) {
                        // Omitted Code ..
                    }
                    //2.3 返回执行周期(Date)
                    return new CronTrigger(cron).nextExecutionTime(triggerContext).toInstant();

                }
        );
    }
}