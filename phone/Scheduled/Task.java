package com.phone.Scheduled;

import com.phone.controller.pojo.Code;
import com.phone.exception.BusinessException;
import com.phone.pojo.Record;
import com.phone.service.CronService;
import com.phone.service.RecordService;
import com.phone.service.UpdateService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.util.ResourceUtils;

import java.io.IOException;
import java.sql.Timestamp;
import java.time.Instant;
import java.time.LocalDateTime;

@Component
public class Task implements Runnable{

    @Autowired
    UpdateService updateService;

    @Autowired
    CronService cronService;

    @Autowired
    RecordService recordService;

    /**
     * 运行python数据分析
     */
    public void RunPython()
    {
        Process process;
        {
            try {
                process = Runtime.getRuntime().exec("python " + ResourceUtils.getFile("classpath:static/main/main.py").getAbsolutePath());
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }

    /**
     * 更新数据库内容
     * @throws IOException
     */
    public  void UpdateDatabase() throws IOException {
        updateService.Update();
    }

    /**
     *
     */
    public void SaveRecord()
    {
        String desc = cronService.getDesc(1);
        Timestamp time = Timestamp.from(Instant.now());
        Record record = new Record(time,desc);
        recordService.saveRecord(record);
    }

    public void test()
    {
        System.out.println("This is Test Program"+ LocalDateTime.now().toLocalTime());

    }


    @Override
    public void run() {
//        test();
//        try{
//          RunPython();
//          }catch (Exception e){
//            throw new BusinessException(Code.ANA_ERR,"运行数据分析时出错");
//        }
//        try {
//            UpdateDatabase();
//        } catch (IOException e) {
//            throw new BusinessException(Code.UPDATE_ERR,"更新数据库时出错");
//        }
//        SaveRecord();
    }
}
