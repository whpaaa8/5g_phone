package com.phone.controller;

import com.phone.controller.pojo.Code;
import com.phone.controller.pojo.Result;
import com.phone.pojo.Cron;
import com.phone.pojo.Record;
import com.phone.service.CronService;
import com.phone.service.RecordService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.util.ResourceUtils;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.List;

/**
 * 用于更新数据库数据
 */
@RestController
@RequestMapping("/update")
public class UpdateController {
    @Autowired
    CronService cronService;
    @Autowired
    RecordService recordService;
    @GetMapping("/id")
    @CrossOrigin
    public Result getDesc(@PathVariable Integer id)
    {
        String desc = cronService.getDesc(id);
        return new Result(Code.GET_OK,desc);
    }

    @GetMapping
    @CrossOrigin
    public Result getCur()
    {
        String desc = cronService.getDesc(1);
        return new Result(Code.GET_OK,desc);
    }

    @GetMapping("/records")
    @CrossOrigin
    public Result getRecords()
    {
        List<Record> records = recordService.getRecords();
        return new Result(Code.GET_OK,records);
    }

    @PutMapping("/id")
    @CrossOrigin
    public Result modify(@PathVariable Integer id)
    {
        Integer flag = cronService.setCron(id);
        if (flag > 0) return  new Result(Code.UPDATE_OK,"修改成功！");
        else return  new Result(Code.UPDATE_ERR,"修改失败！");
    }




}
