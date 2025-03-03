from fasthtml.common import *
from monsterui.all import *




def homepage():
    return Html(
    Head(
        Meta(charset='UTF-8'),
        Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
        Link(href='https://cdn.jsdelivr.net/npm/remixicon@4.5.0/fonts/remixicon.css', rel='stylesheet'),
        Link(rel='stylesheet', href='https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css'),
        Link(rel="icon", type="image/png", href="/assets/favicon.ico"),
        Link(rel='stylesheet', href='/styles/home.css'),
        Title('Bukana | Hotel')
    ),
    Body(
        Nav(
            Div(
                Div(
                    A('Bukana.', href='#'),
                    cls='nav__logo'
                ),
                Div(
                    I(cls='ri-menu-3-line'),
                    id='menu-btn',
                    cls='nav__menu__btn'
                ),
                cls='nav__header'
            ),
                    Ul(
            Li(
                A('HOME', href='#home')
            ),
            Li(
                A('SERVICES', href='#service')
            ),
            Li(
                A('PROPERTIES', href='#property')
            ),
            Li(
                A('SIGN IN', href='#signin')
            ),
            Li(
                A(
                'SIGN UP', 
                style='display: inline-block; padding: 10px 20px; background-color: #333; color: #fff; text-decoration: none; border-radius: 5px; transition: background-color 0.3s ease-in-out, transform 0.2s; cursor: pointer;',
                onmouseover="this.style.backgroundColor='#555'; this.style.transform='scale(1.05)';",
                onmouseout="this.style.backgroundColor='#333'; this.style.transform='scale(1)';",
                onclick="window.location.href='/signup';"
                )
            )

                    ,
            id='nav-links',
            cls='nav__links'
        )

        ),
        Header(
            Div(cls='header__image'),
            Div(
                H1('Easy way to find your dream property'),
                cls='header__content'
            ),
        id='header'
        ),
        Section(
            Div(
                H2('How It Works', cls='section__header'),
                Div(
                    Div(
                        Img(src='/assets/service-1.png', alt='service'),
                        H4('Evaluate Property'),
                        P("Get a detailed assessment of your property's market value and\r\n              potential. Our experts ensure you have the right insights to make\r\n              informed decisions."),
                        cls='service__card'
                    ),
                    Div(
                        Img(src='/assets/service-2.png', alt='service'),
                        H4('Meet Your Agent'),
                        P('Connect with a professional real estate agent who will guide you\r\n              every step of the way. Personalized support makes your buying or\r\n              selling journey effortless.'),
                        cls='service__card'
                    ),
                    Div(
                        Img(src='/assets/service-3.png', alt='service'),
                        H4('Close The Deal'),
                        P('Complete your transaction with confidence and ease. We ensure a\r\n              smooth process so you can secure your dream property without\r\n              hassle.'),
                        cls='service__card'
                    ),
                    cls='service__grid'
                ),
                id='service',
                cls='section__container service__container'
            ),
            cls='service'
        ),
        Section(
            Div(cls='experience__image'),
            Div(
                H2(
                    'We Provide You',
                    Br(),
                    'The Best Experience',
                    cls='section__header'
                ),
                P('Finding the perfect property should be an exciting and hassle-free\r\n          journey, and we are here to make that happen. With our expert\r\n          guidance, personalized support, and in-depth market knowledge, we\r\n          ensure a smooth and seamless real estate experience. Whether you are\r\n          buying, selling, or investing, we provide top-notch services, reliable\r\n          assistance, and the best deals to help you make informed decisions.'),
                Div(
                    Button('ALL PROPERTY', cls='btn',onclick="window.location.href='/signin';"),
                    cls='experience__btn'
                ),
                cls='experience__content'
            ),
            Div(
                Div(
                    H4('550+'),
                    P('Property Build')
                ),
                Div(
                    H4('30+'),
                    P('Awards Gained')
                ),
                Div(
                    H4('20+'),
                    P('Years Of Experience')
                ),
                cls='experience__stats'
            ),
            cls='experience'
        ),
        Section(
            H2('Latest Property', cls='section__header'),
            Div(
                Div(
                    Div(
                        Div(
                            Img(src='assets/property-1.jpg', alt='property'),
                            Div(
                                Div(
                                    H4('Oceanview Villas'),
                                    H5('$1,250,000'),
                                    cls='property__details__header'
                                ),
                                Div(
                                    Div(
                                        Span(
                                            I(cls='ri-hotel-bed-line')
                                        ),
                                        '5'
                                    ),
                                    Div(
                                        Span(
                                            I(cls='ri-showers-line')
                                        ),
                                        '6'
                                    ),
                                    Div(
                                        Span(
                                            I(cls='ri-dashboard-fill')
                                        ),
                                        '4000ft'
                                    ),
                                    cls='property__amenities'
                                ),
                                Div(
                                    Span(
                                        I(cls='ri-map-pin-5-line')
                                    ),
                                    '784 Coastal\r\n                  Drive, USA',
                                    cls='property__location'
                                ),
                                cls='property__details'
                            ),
                            cls='property__card'
                        ),
                        cls='swiper-slide'
                    ),
                    Div(
                        Div(
                            Img(src='assets/property-2.jpg', alt='property'),
                            Div(
                                Div(
                                    H4('Greenwood Estate'),
                                    H5('$850,000'),
                                    cls='property__details__header'
                                ),
                                Div(
                                    Div(
                                        Span(
                                            I(cls='ri-hotel-bed-line')
                                        ),
                                        '4'
                                    ),
                                    Div(
                                        Span(
                                            I(cls='ri-showers-line')
                                        ),
                                        '5'
                                    ),
                                    Div(
                                        Span(
                                            I(cls='ri-dashboard-fill')
                                        ),
                                        '5500ft'
                                    ),
                                    cls='property__amenities'
                                ),
                                Div(
                                    Span(
                                        I(cls='ri-map-pin-5-line')
                                    ),
                                    '4521 Oakwood\r\n                  Lane, Austin',
                                    cls='property__location'
                                ),
                                cls='property__details'
                            ),
                            cls='property__card'
                        ),
                        cls='swiper-slide'
                    ),
                    Div(
                        Div(
                            Img(src='assets/property-3.jpg', alt='property'),
                            Div(
                                Div(
                                    H4('Skyline Tower Apartments'),
                                    H5('$2,500,000'),
                                    cls='property__details__header'
                                ),
                                Div(
                                    Div(
                                        Span(
                                            I(cls='ri-hotel-bed-line')
                                        ),
                                        '6'
                                    ),
                                    Div(
                                        Span(
                                            I(cls='ri-showers-line')
                                        ),
                                        '7'
                                    ),
                                    Div(
                                        Span(
                                            I(cls='ri-dashboard-fill')
                                        ),
                                        '4500ft'
                                    ),
                                    cls='property__amenities'
                                ),
                                Div(
                                    Span(
                                        I(cls='ri-map-pin-5-line')
                                    ),
                                    '2201 West 5th\r\n                  Street, New York',
                                    cls='property__location'
                                ),
                                cls='property__details'
                            ),
                            cls='property__card'
                        ),
                        cls='swiper-slide'
                    ),
                    Div(
                        Div(
                            Img(src='/assets/property-4.jpg', alt='property'),
                            Div(
                                Div(
                                    H4('Maplewood Cottage'),
                                    H5('$540,000'),
                                    cls='property__details__header'
                                ),
                                Div(
                                    Div(
                                        Span(
                                            I(cls='ri-hotel-bed-line')
                                        ),
                                        '4'
                                    ),
                                    Div(
                                        Span(
                                            I(cls='ri-showers-line')
                                        ),
                                        '5'
                                    ),
                                    Div(
                                        Span(
                                            I(cls='ri-dashboard-fill')
                                        ),
                                        '3500ft'
                                    ),
                                    cls='property__amenities'
                                ),
                                Div(
                                    Span(
                                        I(cls='ri-map-pin-5-line')
                                    ),
                                    '980 Maple\r\n                  Street, Denver',
                                    cls='property__location'
                                ),
                                cls='property__details'
                            ),
                            cls='property__card'
                        ),
                        cls='swiper-slide'
                    ),
                    Div(
                        Div(
                            Img(src='/assets/property-5.jpg', alt='property'),
                            Div(
                                Div(
                                    H4('Royal Crest Mansion'),
                                    H5('$4,800,000'),
                                    cls='property__details__header'
                                ),
                                Div(
                                    Div(
                                        Span(
                                            I(cls='ri-hotel-bed-line')
                                        ),
                                        '5'
                                    ),
                                    Div(
                                        Span(
                                            I(cls='ri-showers-line')
                                        ),
                                        '6'
                                    ),
                                    Div(
                                        Span(
                                            I(cls='ri-dashboard-fill')
                                        ),
                                        '5000ft'
                                    ),
                                    cls='property__amenities'
                                ),
                                Div(
                                    Span(
                                        I(cls='ri-map-pin-5-line')
                                    ),
                                    '1789 Kingsway,\r\n                  Beverly Hills',
                                    cls='property__location'
                                ),
                                cls='property__details'
                            ),
                            cls='property__card'
                        ),
                        cls='swiper-slide'
                    ),
                    cls='swiper-wrapper'
                ),
                cls='swiper'
            ),
            id='property',
            cls='section__container property__container'
        ),
        Section(
            H2(
                'Subscribe',
                Br(),
                'Our Newsletter',
                cls='section__header'
            ),
            Form(
                Input(type='text', placeholder='Enter your email'),
                Button('Subscribe', cls='btn'),
                action='/'
            ),
            id='contact',
            cls='subscribe'
        ),
        Footer(
            Div(
                Div(
                    Div(
                        A('Hosale.', href='#'),
                        cls='footer__logo'
                    ),
                    P("At Hosale, we make buying, selling, and investing in properties easy\r\n            and stress-free. Let's turn your real estate goals into reality!"),
                    Ul(
                        Li(
                            A(
                                I(cls='ri-facebook-fill'),
                                href='#'
                            )
                        ),
                        Li(
                            A(
                                I(cls='ri-twitter-fill'),
                                href='#'
                            )
                        ),
                        cls='footer__socials'
                    ),
                    cls='footer__col'
                ),
                Div(
                    H4('OUR COMPANY'),
                    Ul(
                        Li(
                            A('About Us', href='#')
                        ),
                        Li(
                            A('Our Services', href='#')
                        ),
                        Li(
                            A('How It Works', href='#')
                        ),
                        Li(
                            A('Testimonials', href='#')
                        ),
                        Li(
                            A('Contact Us', href='#')
                        ),
                        cls='footer__links'
                    ),
                    cls='footer__col'
                ),
                Div(
                    H4('SUPPORT'),
                    Ul(
                        Li(
                            A('FAQs', href='#')
                        ),
                        Li(
                            A('Property Listings', href='#')
                        ),
                        Li(
                            A("Buyer's Guide", href='#')
                        ),
                        Li(
                            A("Seller's Guide", href='#')
                        ),
                        Li(
                            A('Privacy Policy', href='#')
                        ),
                        Li(
                            A('Terms & Conditions', href='#')
                        ),
                        cls='footer__links'
                    ),
                    cls='footer__col'
                ),
                Div(
                    H4('PROPERTIES'),
                    Div(
                        Img(src='assets/footer.jpg', alt='footer'),
                        Div(
                            H5('Sunset Heights'),
                            P('1256 Maple Avenue, Los Angeles')
                        ),
                        cls='footer__property__detail'
                    ),
                    cls='footer__col'
                ),
                cls='section__container footer__container'
            ),
            Div('Copyright © 2025 Web Design Mastery. All rights reserved.', cls='footer__bar')
        ),
        Script(src='https://unpkg.com/scrollreveal'),
        Script(src='https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js'),
        Script(src='/styles/home.js')
    ),
    lang='en'
)
    
    