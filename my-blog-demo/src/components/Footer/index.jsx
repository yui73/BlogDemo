import { GithubOutlined } from '@ant-design/icons';
import { DefaultFooter } from '@ant-design/pro-layout';

const Footer = () => {
  const defaultMessage = 'XXX的博客';//做后台信息绑定
  const currentYear = new Date().getFullYear();
  return (
    <DefaultFooter
      copyright={`${currentYear} ${defaultMessage}`}
      //博客主的个人联络方式放在下面
      links={[
        // {
        //   key: 'Ant Design Pro',
        //   title: 'Ant Design Pro',
        //   href: 'https://pro.ant.design',
        //   blankTarget: true,
        // },
        {
          key: 'github',
          title: <GithubOutlined />,
          href: 'https://github.com/yui73',
          blankTarget: true,
        },
        // {
        //   key: 'Ant Design',
        //   title: 'Ant Design',
        //   href: 'https://ant.design',
        //   blankTarget: true,
        // },
      ]}
    />
  );
};

export default Footer;
