package com.phone.controller;


import com.phone.controller.pojo.Code;
import com.phone.controller.pojo.Result;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/test")
public class TestController {
    @GetMapping
    @CrossOrigin
    public Result get()
    {
        List<Integer> a =  new ArrayList<>();
        a.add(1);a.add(1);a.add(1);
        List<Integer> b =  new ArrayList<>();
        b.add(2);b.add(2);b.add(2);
        Map<String, List<Integer>> map = new HashMap<>();
        map.put("A",a);
        map.put("B",b);
        return new Result(Code.GET_OK,map);
    }
}
