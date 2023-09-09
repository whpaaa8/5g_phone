package com.phone.service;

import com.phone.pojo.Analysis;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Transactional
public interface AnalysisService {

    /**
     * 保存分析信息
     * @param analysis
     * @return
     */
    public Boolean save(Analysis analysis);

    /**
     * 获取某手机的分析信息
     * @param goods_id
     * @return
     */
    public Analysis getById(String goods_id);
}
