package com.phone.pojo;

public class Analysis {
    private String goods_id;
    private String pos_wordcloud;
    private String neg_wordcloud;
    private String pos_lda;
    private String neg_lda;
    private String pos_topic;
    private String neg_topic;

    public Analysis(String goods_id, String pos_wordcloud, String neg_wordcloud, String pos_lda, String neg_lda, String pos_topic, String neg_topic) {
        this.goods_id = goods_id;
        this.pos_wordcloud = pos_wordcloud;
        this.neg_wordcloud = neg_wordcloud;
        this.pos_lda = pos_lda;
        this.neg_lda = neg_lda;
        this.pos_topic = pos_topic;
        this.neg_topic = neg_topic;
    }

    public String getGoods_id() {
        return goods_id;
    }

    public void setGoods_id(String goods_id) {
        this.goods_id = goods_id;
    }

    public String getPos_wordcloud() {
        return pos_wordcloud;
    }

    public void setPos_wordcloud(String pos_wordcloud) {
        this.pos_wordcloud = pos_wordcloud;
    }

    public String getNeg_wordcloud() {
        return neg_wordcloud;
    }

    public void setNeg_wordcloud(String neg_wordcloud) {
        this.neg_wordcloud = neg_wordcloud;
    }

    public String getPos_lda() {
        return pos_lda;
    }

    public void setPos_lda(String pos_lda) {
        this.pos_lda = pos_lda;
    }

    public String getNeg_lda() {
        return neg_lda;
    }

    public void setNeg_lda(String neg_lda) {
        this.neg_lda = neg_lda;
    }

    public String getPos_topic() {
        return pos_topic;
    }

    public void setPos_topic(String pos_topic) {
        this.pos_topic = pos_topic;
    }

    public String getNeg_topic() {
        return neg_topic;
    }

    public void setNeg_topic(String neg_topic) {
        this.neg_topic = neg_topic;
    }

    @Override
    public String toString() {
        return "Analysis{" +
                "goods_id='" + goods_id + '\'' +
                ", pos_wordcloud='" + pos_wordcloud + '\'' +
                ", neg_wordcloud='" + neg_wordcloud + '\'' +
                ", pos_lda='" + pos_lda + '\'' +
                ", neg_lda='" + neg_lda + '\'' +
                ", pos_topic='" + pos_topic + '\'' +
                ", neg_topic='" + neg_topic + '\'' +
                '}';
    }
}
