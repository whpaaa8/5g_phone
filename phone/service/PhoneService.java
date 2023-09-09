package com.phone.service;

import com.phone.pojo.Phone;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Transactional
public interface PhoneService {

    /***
     * 保存手机数据
     * @param phone
     * @return
     */
    public boolean save(Phone phone);

    /***
     * 删除手机数据
     * @param goods_id
     * @return
     */
    public boolean delete(String goods_id);

    /***
     * 获取某品牌的手机
     * @param brand
     * @return
     */
    public List<Phone> getByBrand(String brand);

    /***
     * 获取所有手机
     * @return
     */
    public List<Phone> getAll();

    /***
     * 获取手机数量
     * @return
     */
    public int getCount();

    /***
     * 判断该手机是否存在
     * @param goods_id
     * @return
     */
    public Boolean isExist(String goods_id);
}
