package com.phone.controller;

import com.phone.controller.pojo.Code;
import com.phone.controller.pojo.Result;
import com.phone.pojo.Analysis;
import com.phone.service.AnalysisService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;


@RestController
@RequestMapping("/analysis")
public class AnalysisController {
    @Autowired
    private AnalysisService analysisService;

    @GetMapping("/{id}")
    @CrossOrigin
    public Result getById(@PathVariable String id)
    {
        Analysis analyses = analysisService.getById(id);
        if (analyses == null) return  new Result(Code.GET_ERR,"还没有对其进行分析！");
        return new Result(Code.GET_OK,analyses);
    }

    @PostMapping
    @CrossOrigin
    public Result save(@RequestBody Analysis analysis)
    {
        Boolean flag = analysisService.save(analysis);
        if (flag) return  new Result(Code.SAVE_OK,"保存分析成功！");
        else return  new Result(Code.SAVE_ERR,"保存分析失败！");
    }


}
