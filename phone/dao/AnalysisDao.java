package com.phone.dao;

import com.phone.pojo.Analysis;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface AnalysisDao {
    @Insert("REPLACE INTO analysis_info (goods_id, pos_wordcloud, neg_wordcloud, pos_lda, neg_lda, pos_topic, neg_topic) values" +
            "(#{goods_id},#{pos_wordcloud},#{neg_wordcloud},#{pos_lda},#{neg_lda},#{pos_topic},#{neg_topic})")
    public int save(Analysis analysis);

    @Select("select * from analysis_info where goods_id = #{goods_id}")
    public Analysis getById(String goods_id);
}
