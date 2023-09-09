package com.phone.controller;

import com.phone.controller.pojo.Code;
import com.phone.controller.pojo.Result;
import com.phone.pojo.Phone;
import com.phone.service.PhoneService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/phones")
public class PhoneController {
    @Autowired
    private PhoneService phoneService;

    @GetMapping("/{brand}")
    @CrossOrigin
    public Result getByBrand(@PathVariable String brand)
    {
        List<Phone> phones = phoneService.getByBrand(brand);
        if (phones.isEmpty())
            return new Result(Code.GET_ERR,null,"没有该品牌的手机信息！");
        else
        return new Result(Code.GET_OK, phones);
    }

    @GetMapping("/count")
    @CrossOrigin
    public Result getCount()
    {
        int count;
        try{
             count = phoneService.getCount();
        } catch (Exception e) {
            return  new Result(Code.GET_ERR,"操作产生错误！");
        }
        return new Result(Code.GET_OK,count);
    }

    @GetMapping
    @CrossOrigin
    public Result getAll()
    {
        List<Phone> phones = phoneService.getAll();
        if (phones.isEmpty())
            return new Result(Code.GET_ERR,null,"没有任何手机信息！");
        else
            return new Result(Code.GET_OK, phones);
    }


    @PostMapping
    public Result save(@RequestBody Phone phone) {
//        return new Result(Code.SAVE_OK,"保存成功！");
      Boolean p = phoneService.save(phone);
      if (p) return new Result(Code.SAVE_OK,"保存成功！");
      else return  new Result(Code.SAVE_ERR,"保存失败！");
    }



    @DeleteMapping("/{id}")
    public Result delete(@PathVariable String id) {
        boolean flag = phoneService.delete(id);
        if (flag) return new Result(Code.DELETE_OK,"保存成功！");
        else return  new Result(Code.DELETE_ERR,"保存失败！");
    }

}