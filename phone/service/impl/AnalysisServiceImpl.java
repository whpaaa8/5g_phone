package com.phone.service.impl;

import com.phone.dao.AnalysisDao;
import com.phone.pojo.Analysis;
import com.phone.service.AnalysisService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
@Service
public class AnalysisServiceImpl implements AnalysisService {
    @Autowired
    private AnalysisDao analysisDao;
    @Override
    public Boolean save(Analysis analysis) {
        int result = analysisDao.save(analysis);
        return result > 0;
    }

    @Override
    public Analysis getById(String goods_id) {
        return analysisDao.getById(goods_id);
    }
}
