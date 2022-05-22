直方图应用
（1）直方图均衡化
①直方图均衡化（全局）
    gary = cv.cvt.Color(img, cv.COLOR_BGR2GRAY)
    dst = cv.equalizeHist(gray)
    cv.imgshow("equalize_demo",dst)
②直方图均衡化（局部自适应）
    gary = cv.cvt.Color(img, cv.COLOR_BGR2GRAY)
    clah = cv.createCLAHE(clipLimit = 2.0, tileGridSize=(8, 8))
    dst = clahe.apply(gray)
    cv.imgshow("clahe_demo",dst)

（2）直方图比较
cv.compareHist(
        直方图1,
        直方图2,
        (1)cv.HISTCMP_BHATTACHARYYA     # 返回巴氏距离
        (2)cv.HISTCMP_CORREL            # 相关性
        (3)cv.HISTCMP_CHISQR            # 卡方
    )

二维直方图显示：
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    hist = cv.calcHist([image], [0, 1], None, [180, 256], [0, 180], 256)
    hist = cv.calcHist([image], [0, 1], None, [32, 32(效果更好)], [0, 180], 256(不能动))
    创建H-S二值图
    cv.normalize(roiHist, roiHist, 0, 255, CV.NORM_MINMAZ)      # 归一化
    dst = cv.calcBackProject([target_hsv][0, 1], roiHist, [0, 180, 0, 255], 1)  # 生成反向投影图像



opencv 小计：
    CVPointPolygonTest()        # 判断一个点是否在轮廓内；
    CPoint是否在CRect中 m_rect.PtInRect(m_point)
分水岭算法：
①距离变换（Distance Transform）
分水岭流程：
（1）输入图像——》（2）灰度——》（3）二值——》（4）距离变换——》（5）寻找种子——》（6）生成Marker——》（7）分水岭变换——》（8）输出图像
    1.  blurred = cv.pyMeanShiftFilteriy(src, 10, 100)
    2.  cv.cvtColor()
    3.  ret binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY|cv.THRESH_OTSU)
    形态学 Rtred = cv.getStructuringElement(cv.MORPH_RECT(3, 3))
    开运算（闭）  mb = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel, iterations=2)
    4.  cv.distanceTransform(mb, cv.DIST_L2(欧几里得), 3)
        cv.distanceTransform(mb, cv.DIST_L1         , 3)
       dis_output = cv.normalize(dist, 0, 1.0, cv.NORM_MINMAX)
       imshow("xxx",dis_output x 50)
    5. threshold(dist, dist.max() x 0.6, 255, cv.THRESH_BINARY)
       np.unit8(surface)        # 格式转换